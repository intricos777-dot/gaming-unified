#include "D3D9Device.h"

extern int g_bUseDynamicBuffers;

OblivionDirect3DDevice9Ex::OblivionDirect3DDevice9Ex(IDirect3D9Ex* D3DInterface, IDirect3DDevice9Ex* D3DDevice) : IDirect3DDevice9Ex() {
	this->D3DInterface = D3DInterface;
	this->D3DDevice = D3DDevice;
}

OblivionDirect3DDevice9Ex::~OblivionDirect3DDevice9Ex() { }

STDMETHODIMP OblivionDirect3DDevice9Ex::QueryInterface(REFIID riid, void **ppvObj) {
	return D3DDevice->QueryInterface(riid, ppvObj);
}

STDMETHODIMP_(ULONG) OblivionDirect3DDevice9Ex::AddRef() {
	return D3DDevice->AddRef();
}

STDMETHODIMP_(ULONG) OblivionDirect3DDevice9Ex::Release() {
	ULONG count = D3DDevice->Release();
	if (count == 0) delete this;
	return count;
}

STDMETHODIMP OblivionDirect3DDevice9Ex::TestCooperativeLevel() {
	return D3DDevice->TestCooperativeLevel();
}

STDMETHODIMP_(UINT) OblivionDirect3DDevice9Ex::GetAvailableTextureMem() {
	return D3DDevice->GetAvailableTextureMem();
}

STDMETHODIMP OblivionDirect3DDevice9Ex::EvictManagedResources() {
	return D3DDevice->EvictManagedResources();
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetDirect3D(IDirect3D9 **ppD3D9) {
	HRESULT hr = D3DDevice->GetDirect3D(ppD3D9);
	if (SUCCEEDED(hr)) *ppD3D9 = (IDirect3D9*)D3DInterface;
	return hr;
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetDeviceCaps(D3DCAPS9 *pCaps) {
	return D3DDevice->GetDeviceCaps(pCaps);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetDisplayMode(UINT iSwapChain, D3DDISPLAYMODE *pMode) {
	return D3DDevice->GetDisplayMode(iSwapChain, pMode);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetCreationParameters(D3DDEVICE_CREATION_PARAMETERS *pParameters) {
	return D3DDevice->GetCreationParameters(pParameters);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetCursorProperties(UINT XHotSpot, UINT YHotSpot, IDirect3DSurface9 *pCursorBitmap) {
	return D3DDevice->SetCursorProperties(XHotSpot, YHotSpot, pCursorBitmap);
}

STDMETHODIMP_(void) OblivionDirect3DDevice9Ex::SetCursorPosition(int X, int Y, DWORD Flags) {
	D3DDevice->SetCursorPosition(X, Y, Flags);
}

STDMETHODIMP_(BOOL) OblivionDirect3DDevice9Ex::ShowCursor(BOOL bShow) {
	return D3DDevice->ShowCursor(bShow);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateAdditionalSwapChain(D3DPRESENT_PARAMETERS *pPresentationParameters, IDirect3DSwapChain9 **pSwapChain) {
	return D3DDevice->CreateAdditionalSwapChain(pPresentationParameters, pSwapChain);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetSwapChain(UINT iSwapChain, IDirect3DSwapChain9 **pSwapChain) {
	return D3DDevice->GetSwapChain(iSwapChain, pSwapChain);
}

COM_DECLSPEC_NOTHROW UINT STDMETHODCALLTYPE OblivionDirect3DDevice9Ex::GetNumberOfSwapChains() {
	return D3DDevice->GetNumberOfSwapChains();
}

STDMETHODIMP OblivionDirect3DDevice9Ex::Reset(D3DPRESENT_PARAMETERS *pPresentationParameters) {
	return ResetEx(pPresentationParameters, NULL);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::Present(CONST RECT *pSourceRect, CONST RECT *pDestRect, HWND hDestWindowOverride, CONST RGNDATA *pDirtyRegion) {
	return D3DDevice->Present(pSourceRect, pDestRect, hDestWindowOverride, pDirtyRegion);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetBackBuffer(UINT iSwapChain, UINT iBackBuffer, D3DBACKBUFFER_TYPE Type, IDirect3DSurface9 **ppBackBuffer) {
	return D3DDevice->GetBackBuffer(iSwapChain, iBackBuffer, Type, ppBackBuffer);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetRasterStatus(UINT iSwapChain, D3DRASTER_STATUS *pRasterStatus) {
	return D3DDevice->GetRasterStatus(iSwapChain, pRasterStatus);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetDialogBoxMode(BOOL bEnableDialogs) {
	return D3DDevice->SetDialogBoxMode(bEnableDialogs);
}

STDMETHODIMP_(void) OblivionDirect3DDevice9Ex::SetGammaRamp(UINT iSwapChain, DWORD Flags, CONST D3DGAMMARAMP *pRamp) {
	return D3DDevice->SetGammaRamp(iSwapChain, Flags, pRamp);
}

STDMETHODIMP_(void) OblivionDirect3DDevice9Ex::GetGammaRamp(UINT iSwapChain, D3DGAMMARAMP *pRamp) {
	return D3DDevice->GetGammaRamp(iSwapChain, pRamp);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateTexture(UINT Width, UINT Height, UINT Levels, DWORD Usage, D3DFORMAT Format, D3DPOOL Pool, IDirect3DTexture9 **ppTexture, HANDLE *pSharedHandle) {
	if (Pool == D3DPOOL_MANAGED)
	{
		Pool = D3DPOOL::D3DPOOL_DEFAULT;
		{
			Usage |= D3DUSAGE_DYNAMIC;
		}
	}
	return D3DDevice->CreateTexture(Width, Height, Levels, Usage, Format, Pool, ppTexture, pSharedHandle);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateVolumeTexture(UINT Width, UINT Height, UINT Depth, UINT Levels, DWORD Usage, D3DFORMAT Format, D3DPOOL Pool, IDirect3DVolumeTexture9 **ppVolumeTexture, HANDLE *pSharedHandle) {
	if (Pool == D3DPOOL_MANAGED)
	{
		Pool = D3DPOOL::D3DPOOL_DEFAULT;
		if (Usage == 0)
		{
			Usage |= D3DUSAGE_DYNAMIC;
		}
	}
	return D3DDevice->CreateVolumeTexture(Width, Height, Depth, Levels, Usage, Format, Pool, ppVolumeTexture, pSharedHandle);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateCubeTexture(UINT EdgeLength, UINT Levels, DWORD Usage, D3DFORMAT Format, D3DPOOL Pool, IDirect3DCubeTexture9 **ppCubeTexture, HANDLE *pSharedHandle) {
	if (Pool == D3DPOOL_MANAGED)
	{
		Pool = D3DPOOL::D3DPOOL_DEFAULT;
		if (Usage == 0)
		{
			Usage |= D3DUSAGE_DYNAMIC;
		}
	}
	return D3DDevice->CreateCubeTexture(EdgeLength, Levels, Usage, Format, Pool, ppCubeTexture, pSharedHandle);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateVertexBuffer(UINT Length, DWORD Usage, DWORD FVF, D3DPOOL Pool, IDirect3DVertexBuffer9 **ppVertexBuffer, HANDLE *pSharedHandle) {
	if (Pool == D3DPOOL_MANAGED)
	{
		Pool = D3DPOOL::D3DPOOL_DEFAULT;
		if (g_bUseDynamicBuffers)
		{
			Usage |= D3DUSAGE_DYNAMIC;
		}
	}
	Usage &= ~D3DUSAGE_SOFTWAREPROCESSING;
	Usage |= D3DUSAGE_WRITEONLY;
	return D3DDevice->CreateVertexBuffer(Length, Usage, FVF, Pool, ppVertexBuffer, pSharedHandle);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateIndexBuffer(UINT Length, DWORD Usage, D3DFORMAT Format, D3DPOOL Pool, IDirect3DIndexBuffer9 **ppIndexBuffer, HANDLE *pSharedHandle) {
	if (Pool == D3DPOOL_MANAGED)
	{
		Pool = D3DPOOL::D3DPOOL_DEFAULT;
		if (g_bUseDynamicBuffers)
		{
			Usage |= D3DUSAGE_DYNAMIC;
		}
	}
	Usage &= ~D3DUSAGE_SOFTWAREPROCESSING;
	Usage |= D3DUSAGE_WRITEONLY;
	return D3DDevice->CreateIndexBuffer(Length, Usage, Format, Pool, ppIndexBuffer, pSharedHandle);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateRenderTarget(UINT Width, UINT Height, D3DFORMAT Format, D3DMULTISAMPLE_TYPE MultiSample, DWORD MultisampleQuality, BOOL Lockable, IDirect3DSurface9 **ppSurface, HANDLE *pSharedHandle) {
	return D3DDevice->CreateRenderTarget(Width, Height, Format, MultiSample, MultisampleQuality, Lockable, ppSurface, pSharedHandle);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateDepthStencilSurface(UINT Width, UINT Height, D3DFORMAT Format, D3DMULTISAMPLE_TYPE MultiSample, DWORD MultisampleQuality, BOOL Discard, IDirect3DSurface9 **ppSurface, HANDLE *pSharedHandle) {
	return D3DDevice->CreateDepthStencilSurface(Width, Height, Format, MultiSample, MultisampleQuality, Discard, ppSurface, pSharedHandle);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::UpdateSurface(IDirect3DSurface9 *pSourceSurface, CONST RECT *pSourceRect, IDirect3DSurface9 *pDestinationSurface, CONST POINT *pDestPoint) {
	return D3DDevice->UpdateSurface(pSourceSurface, pSourceRect, pDestinationSurface, pDestPoint);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::UpdateTexture(IDirect3DBaseTexture9 *pSourceTexture, IDirect3DBaseTexture9 *pDestinationTexture) {
	return D3DDevice->UpdateTexture(pSourceTexture, pDestinationTexture);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetRenderTargetData(IDirect3DSurface9 *pRenderTarget, IDirect3DSurface9 *pDestSurface) {
	return D3DDevice->GetRenderTargetData(pRenderTarget, pDestSurface);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetFrontBufferData(UINT iSwapChain, IDirect3DSurface9 *pDestSurface) {
	return D3DDevice->GetFrontBufferData(iSwapChain, pDestSurface);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::StretchRect(IDirect3DSurface9 *pSourceSurface, CONST RECT *pSourceRect, IDirect3DSurface9 *pDestSurface, CONST RECT *pDestRect, D3DTEXTUREFILTERTYPE Filter) {
	return D3DDevice->StretchRect(pSourceSurface, pSourceRect, pDestSurface, pDestRect, Filter);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::ColorFill(IDirect3DSurface9 *pSurface, CONST RECT *pRect, D3DCOLOR color) {
	return D3DDevice->ColorFill(pSurface, pRect, color);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateOffscreenPlainSurface(UINT Width, UINT Height, D3DFORMAT Format, D3DPOOL Pool, IDirect3DSurface9 **ppSurface, HANDLE *pSharedHandle) {
	if (Pool == D3DPOOL_MANAGED)
	{
		Pool = D3DPOOL::D3DPOOL_DEFAULT;
	}
	return D3DDevice->CreateOffscreenPlainSurface(Width, Height, Format, Pool, ppSurface, pSharedHandle);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetRenderTarget(DWORD RenderTargetIndex, IDirect3DSurface9 *pRenderTarget) {
	return D3DDevice->SetRenderTarget(RenderTargetIndex, pRenderTarget);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetRenderTarget(DWORD RenderTargetIndex, IDirect3DSurface9 **ppRenderTarget) {
	return D3DDevice->GetRenderTarget(RenderTargetIndex, ppRenderTarget);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetDepthStencilSurface(IDirect3DSurface9 *pNewZStencil) {
	return D3DDevice->SetDepthStencilSurface(pNewZStencil);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetDepthStencilSurface(IDirect3DSurface9 **ppZStencilSurface) {
	return D3DDevice->GetDepthStencilSurface(ppZStencilSurface);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::BeginScene() {
	return D3DDevice->BeginScene();
}

STDMETHODIMP OblivionDirect3DDevice9Ex::EndScene() {
	return D3DDevice->EndScene();
}

STDMETHODIMP OblivionDirect3DDevice9Ex::Clear(DWORD Count, CONST D3DRECT *pRects, DWORD Flags, D3DCOLOR Color, float Z, DWORD Stencil) {
	return D3DDevice->Clear(Count, pRects, Flags, Color, Z, Stencil);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetTransform(D3DTRANSFORMSTATETYPE State, CONST D3DMATRIX *pMatrix) {
	return D3DDevice->SetTransform(State, pMatrix);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetTransform(D3DTRANSFORMSTATETYPE State, D3DMATRIX *pMatrix) {
	return D3DDevice->GetTransform(State, pMatrix);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::MultiplyTransform(D3DTRANSFORMSTATETYPE State, CONST D3DMATRIX *pMatrix) {
	return D3DDevice->MultiplyTransform(State, pMatrix);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetViewport(CONST D3DVIEWPORT9 *pViewport) {
	return D3DDevice->SetViewport(pViewport);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetViewport(D3DVIEWPORT9 *pViewport) {
	return D3DDevice->GetViewport(pViewport);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetMaterial(CONST D3DMATERIAL9 *pMaterial) {
	return D3DDevice->SetMaterial(pMaterial);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetMaterial(D3DMATERIAL9 *pMaterial) {
	return D3DDevice->GetMaterial(pMaterial);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetLight(DWORD Index, CONST D3DLIGHT9 *pLight) {
	return D3DDevice->SetLight(Index, pLight);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetLight(DWORD Index, D3DLIGHT9 *pLight) {
	return D3DDevice->GetLight(Index, pLight);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::LightEnable(DWORD Index, BOOL Enable) {
	return D3DDevice->LightEnable(Index, Enable);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetLightEnable(DWORD Index, BOOL *pEnable) {
	return D3DDevice->GetLightEnable(Index, pEnable);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetClipPlane(DWORD Index, CONST float *pPlane) {
	return D3DDevice->SetClipPlane(Index, pPlane);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetClipPlane(DWORD Index, float *pPlane) {
	return D3DDevice->GetClipPlane(Index, pPlane);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetRenderState(D3DRENDERSTATETYPE State, DWORD Value) {
	return D3DDevice->SetRenderState(State, Value);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetRenderState(D3DRENDERSTATETYPE State, DWORD *pValue) {
	return D3DDevice->GetRenderState(State, pValue);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateStateBlock(D3DSTATEBLOCKTYPE Type, IDirect3DStateBlock9 **ppSB) {
	return D3DDevice->CreateStateBlock(Type, ppSB);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::BeginStateBlock() {
	return D3DDevice->BeginStateBlock();
}

STDMETHODIMP OblivionDirect3DDevice9Ex::EndStateBlock(IDirect3DStateBlock9 **ppSB) {
	return D3DDevice->EndStateBlock(ppSB);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetClipStatus(CONST D3DCLIPSTATUS9 *pClipStatus) {
	return D3DDevice->SetClipStatus(pClipStatus);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetClipStatus(D3DCLIPSTATUS9 *pClipStatus) {
	return D3DDevice->GetClipStatus(pClipStatus);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetTexture(DWORD Sampler, IDirect3DBaseTexture9 **ppTexture) {
	return D3DDevice->GetTexture(Sampler, ppTexture);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetTexture(DWORD Sampler, IDirect3DBaseTexture9 *pTexture) {
	return D3DDevice->SetTexture(Sampler, pTexture);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetTextureStageState(DWORD Stage, D3DTEXTURESTAGESTATETYPE Type, DWORD *pValue) {
	return D3DDevice->GetTextureStageState(Stage, Type, pValue);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetTextureStageState(DWORD Stage, D3DTEXTURESTAGESTATETYPE Type, DWORD Value) {
	return D3DDevice->SetTextureStageState(Stage, Type, Value);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetSamplerState(DWORD Sampler, D3DSAMPLERSTATETYPE Type, DWORD *pValue) {
	return D3DDevice->GetSamplerState(Sampler, Type, pValue);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetSamplerState(DWORD Sampler, D3DSAMPLERSTATETYPE Type, DWORD Value) {
	return D3DDevice->SetSamplerState(Sampler, Type, Value);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::ValidateDevice(DWORD *pNumPasses) {
	return D3DDevice->ValidateDevice(pNumPasses);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetPaletteEntries(UINT PaletteNumber, CONST PALETTEENTRY *pEntries) {
	return D3DDevice->SetPaletteEntries(PaletteNumber, pEntries);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetPaletteEntries(UINT PaletteNumber, PALETTEENTRY *pEntries) {
	return D3DDevice->GetPaletteEntries(PaletteNumber, pEntries);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetCurrentTexturePalette(UINT PaletteNumber) {
	return D3DDevice->SetCurrentTexturePalette(PaletteNumber);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetCurrentTexturePalette(UINT *PaletteNumber) {
	return D3DDevice->GetCurrentTexturePalette(PaletteNumber);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetScissorRect(CONST RECT *pRect) {
	return D3DDevice->SetScissorRect(pRect);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetScissorRect(RECT *pRect) {
	return D3DDevice->GetScissorRect(pRect);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetSoftwareVertexProcessing(BOOL bSoftware) {
	return D3DDevice->SetSoftwareVertexProcessing(bSoftware);
}

COM_DECLSPEC_NOTHROW BOOL STDMETHODCALLTYPE OblivionDirect3DDevice9Ex::GetSoftwareVertexProcessing() {
	return D3DDevice->GetSoftwareVertexProcessing();
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetNPatchMode(float nSegments) {
	return D3DDevice->SetNPatchMode(nSegments);
}

COM_DECLSPEC_NOTHROW float STDMETHODCALLTYPE OblivionDirect3DDevice9Ex::GetNPatchMode() {
	return D3DDevice->GetNPatchMode();
}

STDMETHODIMP OblivionDirect3DDevice9Ex::DrawPrimitive(D3DPRIMITIVETYPE PrimitiveType, UINT StartVertex, UINT PrimitiveCount) {
	return D3DDevice->DrawPrimitive(PrimitiveType, StartVertex, PrimitiveCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::DrawIndexedPrimitive(D3DPRIMITIVETYPE PrimitiveType, INT BaseVertexIndex, UINT MinVertexIndex, UINT NumVertices, UINT startIndex, UINT primCount) {
	return D3DDevice->DrawIndexedPrimitive(PrimitiveType, BaseVertexIndex, MinVertexIndex, NumVertices, startIndex, primCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::DrawPrimitiveUP(D3DPRIMITIVETYPE PrimitiveType, UINT PrimitiveCount, CONST void *pVertexStreamZeroData, UINT VertexStreamZeroStride) {
	return D3DDevice->DrawPrimitiveUP(PrimitiveType, PrimitiveCount, pVertexStreamZeroData, VertexStreamZeroStride);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::DrawIndexedPrimitiveUP(D3DPRIMITIVETYPE PrimitiveType, UINT MinVertexIndex, UINT NumVertices, UINT PrimitiveCount, CONST void *pIndexData, D3DFORMAT IndexDataFormat, CONST void *pVertexStreamZeroData, UINT VertexStreamZeroStride) {
	return D3DDevice->DrawIndexedPrimitiveUP(PrimitiveType, MinVertexIndex, NumVertices, PrimitiveCount, pIndexData, IndexDataFormat, pVertexStreamZeroData, VertexStreamZeroStride);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::ProcessVertices(UINT SrcStartIndex, UINT DestIndex, UINT VertexCount, IDirect3DVertexBuffer9 *pDestBuffer, IDirect3DVertexDeclaration9 *pVertexDecl, DWORD Flags) {
	return D3DDevice->ProcessVertices(SrcStartIndex, DestIndex, VertexCount, pDestBuffer, pVertexDecl, Flags);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateVertexDeclaration(CONST D3DVERTEXELEMENT9 *pVertexElements, IDirect3DVertexDeclaration9 **ppDecl) {
	return D3DDevice->CreateVertexDeclaration(pVertexElements, ppDecl);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetVertexDeclaration(IDirect3DVertexDeclaration9 *pDecl) {
	return D3DDevice->SetVertexDeclaration(pDecl);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetVertexDeclaration(IDirect3DVertexDeclaration9 **ppDecl) {
	return D3DDevice->GetVertexDeclaration(ppDecl);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetFVF(DWORD FVF) {
	return D3DDevice->SetFVF(FVF);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetFVF(DWORD *pFVF) {
	return D3DDevice->GetFVF(pFVF);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateVertexShader(CONST DWORD *pFunction, IDirect3DVertexShader9 **ppShader) {
	return D3DDevice->CreateVertexShader(pFunction, ppShader);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetVertexShader(IDirect3DVertexShader9 *pShader) {
	return D3DDevice->SetVertexShader(pShader);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetVertexShader(IDirect3DVertexShader9 **ppShader) {
	return D3DDevice->GetVertexShader(ppShader);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetVertexShaderConstantF(UINT StartRegister, CONST float *pConstantData, UINT Vector4fCount) {
	return D3DDevice->SetVertexShaderConstantF(StartRegister, pConstantData, Vector4fCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetVertexShaderConstantF(UINT StartRegister, float *pConstantData, UINT Vector4fCount) {
	return D3DDevice->GetVertexShaderConstantF(StartRegister, pConstantData, Vector4fCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetVertexShaderConstantI(UINT StartRegister, CONST int *pConstantData, UINT Vector4iCount) {
	return D3DDevice->SetVertexShaderConstantI(StartRegister, pConstantData, Vector4iCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetVertexShaderConstantI(UINT StartRegister, int *pConstantData, UINT Vector4iCount) {
	return D3DDevice->GetVertexShaderConstantI(StartRegister, pConstantData, Vector4iCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetVertexShaderConstantB(UINT StartRegister, CONST BOOL *pConstantData, UINT BoolCount) {
	return D3DDevice->SetVertexShaderConstantB(StartRegister, pConstantData, BoolCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetVertexShaderConstantB(UINT StartRegister, BOOL *pConstantData, UINT BoolCount) {
	return D3DDevice->GetVertexShaderConstantB(StartRegister, pConstantData, BoolCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetStreamSource(UINT StreamNumber, IDirect3DVertexBuffer9 *pStreamData, UINT OffsetInBytes, UINT Stride) {
	return D3DDevice->SetStreamSource(StreamNumber, pStreamData, OffsetInBytes, Stride);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetStreamSource(UINT StreamNumber, IDirect3DVertexBuffer9 **ppStreamData, UINT *pOffsetInBytes, UINT *pStride) {
	return D3DDevice->GetStreamSource(StreamNumber, ppStreamData, pOffsetInBytes, pStride);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetStreamSourceFreq(UINT StreamNumber, UINT Setting) {
	return D3DDevice->SetStreamSourceFreq(StreamNumber, Setting);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetStreamSourceFreq(UINT StreamNumber, UINT *pSetting) {
	return D3DDevice->GetStreamSourceFreq(StreamNumber, pSetting);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetIndices(IDirect3DIndexBuffer9 *pIndexData) {
	return D3DDevice->SetIndices(pIndexData);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetIndices(IDirect3DIndexBuffer9 **ppIndexData) {
	return D3DDevice->GetIndices(ppIndexData);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreatePixelShader(CONST DWORD *pFunction, IDirect3DPixelShader9 **ppShader) {
	return D3DDevice->CreatePixelShader(pFunction, ppShader);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetPixelShader(IDirect3DPixelShader9 *pShader) {
	return D3DDevice->SetPixelShader(pShader);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetPixelShader(IDirect3DPixelShader9 **ppShader) {
	return D3DDevice->GetPixelShader(ppShader);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetPixelShaderConstantF(UINT StartRegister, CONST float *pConstantData, UINT Vector4fCount) {
  return D3DDevice->SetPixelShaderConstantF(StartRegister, pConstantData, Vector4fCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetPixelShaderConstantF(UINT StartRegister, float *pConstantData, UINT Vector4fCount) {
	return D3DDevice->GetPixelShaderConstantF(StartRegister, pConstantData, Vector4fCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetPixelShaderConstantI(UINT StartRegister, CONST int *pConstantData, UINT Vector4iCount) {
	return D3DDevice->SetPixelShaderConstantI(StartRegister, pConstantData, Vector4iCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetPixelShaderConstantI(UINT StartRegister, int *pConstantData, UINT Vector4iCount) {
	return D3DDevice->GetPixelShaderConstantI(StartRegister, pConstantData, Vector4iCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetPixelShaderConstantB(UINT StartRegister, CONST BOOL *pConstantData, UINT  BoolCount) {
	return D3DDevice->SetPixelShaderConstantB(StartRegister, pConstantData, BoolCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetPixelShaderConstantB(UINT StartRegister, BOOL *pConstantData, UINT BoolCount) {
	return D3DDevice->GetPixelShaderConstantB(StartRegister, pConstantData, BoolCount);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::DrawRectPatch(UINT Handle, CONST float *pNumSegs, CONST D3DRECTPATCH_INFO *pRectPatchInfo) {
	return D3DDevice->DrawRectPatch(Handle, pNumSegs, pRectPatchInfo);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::DrawTriPatch(UINT Handle, CONST float *pNumSegs, CONST D3DTRIPATCH_INFO *pTriPatchInfo) {
	return D3DDevice->DrawTriPatch(Handle, pNumSegs, pTriPatchInfo);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::DeletePatch(UINT Handle) {
	return D3DDevice->DeletePatch(Handle);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateQuery(D3DQUERYTYPE Type, IDirect3DQuery9 **ppQuery) {
	return D3DDevice->CreateQuery(Type, ppQuery);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetConvolutionMonoKernel(UINT width, UINT height, float * rows, float * columns) {
	return D3DDevice->SetConvolutionMonoKernel(width, height, rows, columns);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::ComposeRects(IDirect3DSurface9 * pSrc, IDirect3DSurface9 * pDst, IDirect3DVertexBuffer9 * pSrcRectDescs, UINT NumRects, IDirect3DVertexBuffer9 * pDstRectDescs, D3DCOMPOSERECTSOP Operation, int Xoffset, int Yoffset) {
	return D3DDevice->ComposeRects(pSrc, pDst, pSrcRectDescs, NumRects, pDstRectDescs, Operation, Xoffset, Yoffset);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::PresentEx(CONST RECT * pSourceRect, CONST RECT * pDestRect, HWND hDestWindowOverride, CONST RGNDATA * pDirtyRegion, DWORD dwFlags) {
	return D3DDevice->PresentEx(pSourceRect, pDestRect, hDestWindowOverride, pDirtyRegion, dwFlags);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetGPUThreadPriority(INT * pPriority) {
	return D3DDevice->GetGPUThreadPriority(pPriority);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetGPUThreadPriority(INT Priority) {
	return D3DDevice->SetGPUThreadPriority(Priority);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::WaitForVBlank(UINT iSwapChain) {
	return D3DDevice->WaitForVBlank(iSwapChain);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CheckResourceResidency(IDirect3DResource9 ** pResourceArray, UINT32 NumResources) {
	return D3DDevice->CheckResourceResidency(pResourceArray, NumResources);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::SetMaximumFrameLatency(UINT MaxLatency) {
	return D3DDevice->SetMaximumFrameLatency(MaxLatency);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetMaximumFrameLatency(UINT * pMaxLatency) {
	return D3DDevice->GetMaximumFrameLatency(pMaxLatency);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CheckDeviceState(HWND hDestinationWindow) {
	return D3DDevice->CheckDeviceState(hDestinationWindow);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateRenderTargetEx(UINT Width, UINT Height, D3DFORMAT Format, D3DMULTISAMPLE_TYPE MultiSample, DWORD MultisampleQuality, BOOL Lockable, IDirect3DSurface9 ** ppSurface, HANDLE * pSharedHandle, DWORD Usage) {
	return D3DDevice->CreateRenderTargetEx(Width, Height, Format, MultiSample, MultisampleQuality, Lockable, ppSurface, pSharedHandle, Usage);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateOffscreenPlainSurfaceEx(UINT Width, UINT Height, D3DFORMAT Format, D3DPOOL Pool, IDirect3DSurface9 ** ppSurface, HANDLE * pSharedHandle, DWORD Usage) {
	if (Pool == D3DPOOL_MANAGED)
	{
		Pool = D3DPOOL::D3DPOOL_DEFAULT;
		if (Usage == 0)
		{
			Usage |= D3DUSAGE_DYNAMIC;
		}
	}
	return D3DDevice->CreateOffscreenPlainSurfaceEx(Width, Height, Format, Pool, ppSurface, pSharedHandle, Usage);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::CreateDepthStencilSurfaceEx(UINT Width, UINT Height, D3DFORMAT Format, D3DMULTISAMPLE_TYPE MultiSample, DWORD MultisampleQuality, BOOL Discard, IDirect3DSurface9 ** ppSurface, HANDLE * pSharedHandle, DWORD Usage) {
	return D3DDevice->CreateDepthStencilSurfaceEx(Width, Height, Format, MultiSample, MultisampleQuality, Discard, ppSurface, pSharedHandle, Usage);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::ResetEx(D3DPRESENT_PARAMETERS * pPresentationParameters, D3DDISPLAYMODEEX * pFullscreenDisplayMode) {
	return D3DDevice->ResetEx(pPresentationParameters, pFullscreenDisplayMode);
}

STDMETHODIMP OblivionDirect3DDevice9Ex::GetDisplayModeEx(UINT iSwapChain, D3DDISPLAYMODEEX * pMode, D3DDISPLAYROTATION * pRotation) {
	return D3DDevice->GetDisplayModeEx(iSwapChain, pMode, pRotation);
}
