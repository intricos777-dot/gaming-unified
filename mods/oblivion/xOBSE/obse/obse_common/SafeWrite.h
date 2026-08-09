#pragma once
template<typename T>
concept IntegerOrPointer = std::is_same<T,UInt32>::value || std::is_same<T, unsigned int>::value || (std::is_pointer<T>::value && std::is_function<std::remove_pointer_t<T>>::value);

void SafeWrite8(UInt32 addr, UInt32 data);
void SafeWrite16(UInt32 addr, UInt32 data);
void __declspec(noinline) SafeWrite32Inner(UInt32 addr, UInt32 data);
void SafeWriteBuf(UInt32 addr, void * data, UInt32 len);

template<IntegerOrPointer T>
__forceinline void  SafeWrite32(UInt32 addr, T data){
	if constexpr (std::is_pointer_v<T>) {
        SafeWrite32Inner(addr, reinterpret_cast<UInt32>(data));
    } else {
        SafeWrite32Inner(addr, static_cast<UInt32>(data));
    }
}


// 5 bytes
void WriteRelJump(UInt32 jumpSrc, UInt32 jumpTgt);
void WriteRelCall(UInt32 jumpSrc, UInt32 jumpTgt);

// 6 bytes
void WriteRelJz(UInt32 jumpSrc, UInt32 jumpTgt);
void WriteRelJnz(UInt32 jumpSrc, UInt32 jumpTgt);
void WriteRelJle(UInt32 jumpSrc, UInt32 jumpTgt);

//Write arbitrary nop
void WriteNop(UInt32 nopAddr, UInt8 numOfByte);
//PAtch calls to address in a certain range
void PatchCallsInRange(UInt32 start, UInt32 end, UInt32 CallToPatch, UInt32 HookCall);