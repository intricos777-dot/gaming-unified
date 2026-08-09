#pragma once

#include "D3D9Hook.h"
#include "D3D9Device.h"
#include "obse_common/SafeWrite.h"

static const UInt32 kCreateDeviceHook = 0x0076A542;
static const UInt32 kCreateDeviceReturn = 0x0076A547;
static const UInt32 kDirect3DCreate9Hook = 0x00761E2D;
static const UInt32 kDirect3DCreate9Return = 0x00761E33;

int _bUseFlipExSwapMode = 0;

int _bUseEx = 0;

IDirect3D9* STDMETHODCALLTYPE Direct3DCreate9(UINT SDKVersion)
{
	IDirect3D9Ex* pD3D = NULL;

	_MESSAGE(" Redirecting Direct3DCreate9 to Direct3DCreate9Ex");
	HRESULT hr = Direct3DCreate9Ex(SDKVersion, &pD3D);

	return pD3D;
}

HRESULT STDMETHODCALLTYPE Direct3DCreate9Ex(UINT SDKVersion, IDirect3D9Ex** ppD3D)
{
	// Get d3d9.dll
	_MESSAGE("  Loading d3d9.dll");
	HMODULE d3d9 = GetModuleHandleA("d3d9.dll");
	if (!d3d9)
		d3d9 = LoadLibraryA("d3d9.dll");

	if (!d3d9)
	{
		_MESSAGE("   ! Failed to load d3d9.dll!");
		return E_FAIL;
	}

	_MESSAGE("  Getting Direct3DCreate9Ex proc address");
	auto pDirect3DCreate9 = (decltype(&Direct3DCreate9))GetProcAddress(d3d9, "Direct3DCreate9");
	auto pDirect3DCreate9Ex = (decltype(&Direct3DCreate9Ex))GetProcAddress(d3d9, "Direct3DCreate9Ex");
	
	if (!pDirect3DCreate9Ex)
	{
		_MESSAGE("  ! Failed to find Direct3DCreate9Ex in current d3d9.dll! Falling back to Direct3DCreate9.");
		if (!pDirect3DCreate9)
		{
			_MESSAGE("   Failed to find Direct3DCreate9 in current d3d9.dll!");
			return E_FAIL;
		}
		*ppD3D = (IDirect3D9Ex*)pDirect3DCreate9(SDKVersion);
		return E_FAIL;
	}

	_MESSAGE("  Calling Direct3DCreate9Ex");
	HRESULT hr = pDirect3DCreate9Ex(SDKVersion, ppD3D);

	_bUseEx = SUCCEEDED(hr);

	return hr;
}

HRESULT STDMETHODCALLTYPE CreateDeviceEx(IDirect3D9Ex* D3DInterface, UINT Adapter, D3DDEVTYPE DeviceType, HWND hFocusWindow, DWORD BehaviorFlags, D3DPRESENT_PARAMETERS* pPresentationParameters, D3DDISPLAYMODEEX* pFullscreenDisplayMode, IDirect3DDevice9Ex** ppReturnedDeviceInterface)
{
	if (_bUseFlipExSwapMode)
	{
		_MESSAGE("  FlipEx enabled");
		pPresentationParameters->SwapEffect = D3DSWAPEFFECT::D3DSWAPEFFECT_FLIPEX;
		pPresentationParameters->Flags &= ~D3DPRESENTFLAG_LOCKABLE_BACKBUFFER;
	}
	_MESSAGE("  Creating D3D9Ex device");
	HRESULT R = D3DInterface->CreateDeviceEx(Adapter, DeviceType, hFocusWindow, BehaviorFlags, pPresentationParameters, pFullscreenDisplayMode, ppReturnedDeviceInterface);

	*ppReturnedDeviceInterface = new OblivionDirect3DDevice9Ex(D3DInterface, *ppReturnedDeviceInterface);

	return R;
}

HRESULT STDMETHODCALLTYPE CreateDevice(IDirect3D9Ex* D3DInterface, UINT Adapter, D3DDEVTYPE DeviceType, HWND hFocusWindow, DWORD BehaviorFlags, D3DPRESENT_PARAMETERS* pPresentationParameters, IDirect3DDevice9Ex** ppReturnedDeviceInterface) 
{
	if (_bUseEx)
	{
		D3DDISPLAYMODEEX* pFullscreenDisplayMode;
		D3DDISPLAYMODEEX displayModeEx;

		if (pPresentationParameters->Windowed == FALSE)
		{
			displayModeEx.Format = pPresentationParameters->BackBufferFormat;
			displayModeEx.Width = pPresentationParameters->BackBufferWidth;
			displayModeEx.Height = pPresentationParameters->BackBufferHeight;
			displayModeEx.RefreshRate = pPresentationParameters->FullScreen_RefreshRateInHz;
			displayModeEx.ScanLineOrdering = D3DSCANLINEORDERING_PROGRESSIVE;
			displayModeEx.Size = sizeof(D3DDISPLAYMODEEX);
			pFullscreenDisplayMode = &displayModeEx;
		}
		else
		{
			pFullscreenDisplayMode = nullptr;
		}

		_MESSAGE(" Redirecting CreateDevice to CreateDeviceEx");
		HRESULT R = CreateDeviceEx(D3DInterface, Adapter, DeviceType, hFocusWindow, BehaviorFlags, pPresentationParameters, pFullscreenDisplayMode, (IDirect3DDevice9Ex**)ppReturnedDeviceInterface);
		return R;
	}
	else
	{
		_MESSAGE(" Falling back to CreateDevice");
		HRESULT R = D3DInterface->CreateDevice(Adapter, DeviceType, hFocusWindow, BehaviorFlags, pPresentationParameters, (IDirect3DDevice9**)ppReturnedDeviceInterface);
		MessageBox(NULL, "Failed to create D3D9Ex, falling back to normal D3D9.\nFlipEx will not work!\n\nYou're probably using ENB.\nENB is fully incompatible with D3D9Ex as it doesn't implement the necessary functions in d3d9.dll.\nRemove ENB if you want to use D3D9Ex.\nOr set bUseD3D9Ex = 0 in oblivion_display_tweaks.ini to use ENB with this plugin without the warning.", "Oblivion Display Tweaks", MB_TASKMODAL | MB_SETFOREGROUND | MB_ICONERROR | MB_OK);

		return R;
	}
}

static __declspec(naked) void Direct3DCreate9Hook()
{

	__asm
	{
		push	20h
		call	Direct3DCreate9
		test	eax, eax
		jmp		kDirect3DCreate9Return
	}

}

static __declspec(naked) void CreateDeviceHook()
{

	__asm
	{
		mov		eax, [ecx + 0x40]
		call	CreateDevice
		jmp		kCreateDeviceReturn
	}

}

void HookD3D9(int bUseFlipExSwapMode) 
{
	_bUseFlipExSwapMode = bUseFlipExSwapMode;
	SafeWriteBuf(kDirect3DCreate9Hook, "\x90\x90\x90\x90\x90\x90", 6);
	WriteRelJump(kDirect3DCreate9Hook, (UInt32)Direct3DCreate9Hook);
	WriteRelJump(kCreateDeviceHook, (UInt32)CreateDeviceHook);
}

