#pragma once

OBSEConsoleInterface* g_con = NULL;

float* g_FPSGlobal = (float*)(0xB33E94);
bool* g_bFullScreen = (bool*)(0xB06C74);
float* g_fDefaultFOV = (float*)(0xB0313C);

float fMenuDefaultFOV = 75.f;

UINT32 OriginalFunction;

//float* fMaxTime = (float*)0xB097C0;
float* fMaxTime = (float*)0xB2E2E8;

int g_iTickFix = 0;
int g_bFOVFix = 0;
int g_bDialogFOVFix = 0;
int g_bFastExit = 0;
int g_bBorderless = 0;
int g_bForceD3D9Ex = 0;
int g_bUseFlipExSwapMode = 0;
int g_bUseDynamicBuffers = 0;
int g_bFPSFix = 0;
int g_iMaxFPS = 1;
int g_iMinFPS = 1;
int g_bfMaxTime;
float g_iDialogFixMult = 1;
float DefaultMaxTime = 0;
double	DesiredMax = 1;
double	DesiredMin = 1;

#include "FPSTimer.h"
#include "obse/GameMenus.h"
#include "D3D9Hook.h"
#include "CommandTable.h"
#pragma comment(lib, "winmm.lib")

void FastExit()
{
	if (g_con)
		g_con->RunScriptLine("con_SaveINI");

	TerminateProcess(GetCurrentProcess(), 0);
}

 typedef bool (*_IsMenuMode)(void);
 const _IsMenuMode IsMenuMode = (_IsMenuMode)0x00578F60;

void UpdateHook() 
{
	if (g_bFPSFix)
	{
		double Delta = GetFPSCounterMiliSeconds();
		if (IsMenuMode())
		{
			Menu* dialogMenu = GetMenuByType(kMenuType_Dialog);
			if (dialogMenu)
			{
				*g_FPSGlobal = (Delta > 0) ? ((Delta < DesiredMin) ? ((Delta > DesiredMax / g_iDialogFixMult) ? Delta : DesiredMax / g_iDialogFixMult) : DesiredMin) : 0;
				if (g_bfMaxTime)
					*fMaxTime = ((Delta > 0 && Delta < DefaultMaxTime && Delta > DesiredMax) ? Delta / 1000 : DefaultMaxTime / 1000);
			}
			else
			{
				*g_FPSGlobal = 0;
				*fMaxTime = DefaultMaxTime / 1000;
			}
		}
		else
		{
			*g_FPSGlobal = (Delta > 0) ? ((Delta < DesiredMin) ? ((Delta > DesiredMax) ? Delta : DesiredMax) : DesiredMin) : 0;
			if (g_bfMaxTime)
				*fMaxTime = ((Delta > 0 && Delta < DefaultMaxTime && Delta > DesiredMax) ? Delta / 1000 : DefaultMaxTime / 1000);
		}
	}
}

void __declspec(naked) UpdateHookHandler()
{

	__asm {
		pushad
		call	UpdateHook
		popad
		mov		ecx, [eax]
		mov		edx, [ecx + 0x0C]
		jmp[OriginalFunction]
	}

}

static const UInt32 kFOVHook = 0x004116FA;
static const UInt32 kFOVReturn = 0x00411700;

static const UInt32 kDialogFOVFixHook = 0x0066C710;
static const UInt32 kDialogFOVFixReturn = 0x0066C716;

void __declspec(naked) FOVHook()
{

	__asm {
		fld fMenuDefaultFOV
		jmp kFOVReturn
	}
	// Replace with original code afterwards to be safe
	SafeWriteBuf(kFOVHook, "\xD9\x05\x3C\x31\xB0\x00", 6);
}

void __declspec(naked) DialogFOVFix()
{
	static const float fov = *g_fDefaultFOV;
	__asm {
		fld fov
		jmp kDialogFOVFixReturn
	}

}

void HookUpdate()
{
	WriteRelJump((UINT32)0x0040F1A3, (UInt32)&UpdateHookHandler);
	OriginalFunction = 0x0040F1A8;
}

void HookFOV()
{
	// hook SceneGraph so FOV doesn't mess up the menus
	SafeWriteBuf(kFOVHook, "\x90\x90\x90\x90\x90\x90", 6);
	WriteRelJump(kFOVHook, (UInt32)&FOVHook);

	if (g_bDialogFOVFix)
	{
		// Fix hardcoded 75.0 FOV value in dialog zoom calculation that caused the ugly snap when starting/ending a conversation
		// with FOV different than 75.
		SafeWriteBuf(kDialogFOVFixHook, "\x90\x90\x90\x90\x90\x90", 6);
		WriteRelJump(kDialogFOVFixHook, (UInt32)&DialogFOVFix);
	}
}

void HookWindow()
{
	// Set window position to 0,0
	SafeWriteBuf(0x0049846F, "\xBA\x00\x00\x00\x00\x90", 6);
	SafeWriteBuf(0x00498478, "\xB9\x00\x00\x00\x00\x90", 6);
	// Window styles
	SafeWrite32(0x0040E7C0, WS_POPUP);
	SafeWrite32(0x0040E805, WS_POPUP | WS_VISIBLE);
}

void DoPatches()
{
	if (g_iTickFix > 0) {
		_MESSAGE("Tick Fix %u enabled", g_iTickFix);
		FPSStartCounter();
		if (g_iTickFix > 1)
		{
			timeBeginPeriod(1);
			SafeWrite32(0xA280D0, (UInt32)timeGetTime);
		}
		else
		{
			SafeWrite32(0xA280D0, (UInt32)ReturnCounter);
		}

		if (g_bFPSFix)
		{
			_MESSAGE("FPS Fix enabled");
			DesiredMax = 1000 / double(g_iMaxFPS);
			DesiredMin = 1000 / double(g_iMinFPS);
			DefaultMaxTime = (*fMaxTime) * 1000;
			HookUpdate();
		}
	}
	if (g_bFOVFix > 0)
	{
		_MESSAGE("FOV Fix enabled");
		HookFOV();
	}
	if (g_bFastExit)
	{
		_MESSAGE("Fast Exit enabled");
		WriteRelJump(0x0040F48C, (UInt32)FastExit);
	}
	if (g_bBorderless)
	{
		//*g_bFullScreen = 0;
		_MESSAGE("Borderless windowed enabled");
		HookWindow();
	}
	if (g_bForceD3D9Ex)
	{
		_MESSAGE("Use D3D9Ex enabled");
		HookD3D9(g_bUseFlipExSwapMode);
	}
}
