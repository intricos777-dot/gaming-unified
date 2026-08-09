#pragma once

#include "obse/PluginAPI.h"
#include "obse/CommandTable.h"
#include "obse_common/SafeWrite.cpp"
#include "obse/GameAPI.h"

#include "obse/ParamInfos.h"
#include "obse/Script.h"
#include "obse/GameObjects.h"
#include "main.h"
#include <string>

IDebugLog		gLog("oblivion_display_tweaks.log");
PluginHandle	g_pluginHandle = kPluginHandle_Invalid;

extern "C" {

bool OBSEPlugin_Query(const OBSEInterface* obse, PluginInfo* info)
{
	_MESSAGE("Plugin query...");

	// fill out the info structure
	info->infoVersion = PluginInfo::kInfoVersion;
	info->name = "oblivion_display_tweaks";
	info->version = 1;

	// version checks
	if(!obse->isEditor)
	{
		if(obse->obseVersion < 21)
		{
			_ERROR("OBSE version too old (got %08X expected at least %08X)", obse->obseVersion, 21);
			return false;
		}

		if(obse->oblivionVersion != OBLIVION_VERSION)
		{
			_ERROR("incorrect Oblivion version (got %08X need %08X)", obse->oblivionVersion, OBLIVION_VERSION);
			return false;
		}
	}
	else
	{
		_MESSAGE(" Not loading in editor");
		// don't load in editor
		return false;
	}

	// version checks pass
	_MESSAGE(" Plugin query passed");
	return true;
}

bool OBSEPlugin_Load(const OBSEInterface* obse)
{
	_MESSAGE("Oblivion Display Tweaks version %u", 1);

	g_pluginHandle = obse->GetPluginHandle();

	char iniDir[MAX_PATH];

	GetModuleFileName(GetModuleHandle(NULL), iniDir, MAX_PATH);
	strcpy((char*)(strrchr(iniDir, '\\') + 1), "Data\\OBSE\\Plugins\\oblivion_display_tweaks.ini");
	_MESSAGE("Loading settings from %s", iniDir);

	g_iTickFix = GetPrivateProfileInt("Main", "iTickFix", 0, iniDir);
	g_bFOVFix = GetPrivateProfileInt("Main", "bFOVFix", 0, iniDir);
	g_bFastExit = GetPrivateProfileInt("Main", "bFastExit", 0, iniDir);
	g_bBorderless = GetPrivateProfileInt("Main", "bBorderless", 0, iniDir);

	g_bForceD3D9Ex = GetPrivateProfileInt("DirectX", "bUseD3D9Ex", 0, iniDir);
	g_bUseFlipExSwapMode = GetPrivateProfileInt("D3D9Ex", "bUseFlipExSwapMode", 0, iniDir);
	g_bUseDynamicBuffers = GetPrivateProfileInt("D3D9Ex", "bUseDynamicBuffers", 0, iniDir);

	g_bFPSFix = GetPrivateProfileInt("TickFix", "bFPSFix", 0, iniDir);
	
	g_iMaxFPS = GetPrivateProfileInt("FPSFix", "iMaxFPSTolerance", 59, iniDir);
	g_iMinFPS = GetPrivateProfileInt("FPSFix", "iMinFPSTolerance", 20, iniDir);
	g_bfMaxTime = GetPrivateProfileInt("FPSFix", "bfMaxTime", 1, iniDir);

	g_bDialogFOVFix = GetPrivateProfileInt("FOVFix", "bDialogFOVFix", 0, iniDir);

	char floatbuffer[0x40];
	GetPrivateProfileString("FPSFix", "fDialogFixMult", "2.0000", floatbuffer, 0x3F, iniDir);
	g_iDialogFixMult = atof(floatbuffer);

	g_con = (OBSEConsoleInterface*)obse->QueryInterface(kInterface_Console);

	//*g_fDefaultFOV = fMenuDefaultFOV;

	DoPatches();

	return true;
}

};
