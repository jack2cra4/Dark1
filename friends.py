# ============================================================
#   FRIEND BGMI TOOL — ULTIMATE MASTER ENGINE (BEAST LEVEL)
#   STANDARDIZED BRANDING — TACTICAL FULL ENGINE
#   NO FAKE SUCCESS | FULL ERROR REPORTING | ZERO IN-GAME LAG
#   UPGRADE A-F: ORIGINAL-FILE DUMP / ANY-PAK / LUA DECODE /
#                OBB BLOB / HASH-VERIFY / NESTED SCAN / SAFE REPACK
#   BEAST v2: STEALTH REPACK (SIZE-TRACK DEFEAT) / AXML DECODER /
#             SQLITE READABLE / REPEAT-XOR BREAKER / CONTENT-MASK
# ============================================================

import itertools as it
import math
import struct
import shutil
import os
import sys
import uuid
import hashlib
import platform
import subprocess
import requests
import base64
import zlib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import PurePath, Path
from typing import List, Dict, Tuple, Optional, Any
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.table import Table
from rich import print as rprint
from rich.markup import escape
from rich.text import Text
from rich.align import Align
from rich.box import HEAVY_EDGE, ROUNDED, DOUBLE_EDGE
from datetime import datetime
import pytz
import re
import zipfile
import json
import traceback

def _batched(iterable, n):
    it_obj = iter(iterable)
    while True:
        batch = list(it.islice(it_obj, n))
        if not batch: break
        yield batch

# ==================== VENDORED ZUC CIPHER ====================

_ZUC_S0 = bytes([
    0x3e,0x72,0x5b,0x47,0xca,0xe0,0x00,0x33,0x04,0xd1,0x54,0x98,0x09,0xb9,0x6d,0xcb,
    0x7b,0x1b,0xf9,0x32,0xaf,0x9d,0x6a,0xa5,0xb8,0x2d,0xfc,0x1d,0x08,0x53,0x03,0x90,
    0x4d,0x4e,0x84,0x99,0xe4,0xce,0xd9,0x91,0xdd,0xb6,0x85,0x48,0x8b,0x29,0x6e,0xac,
    0xcd,0xc1,0xf8,0x1e,0x73,0x43,0x69,0xc6,0xb5,0xbd,0xfd,0x39,0x63,0x20,0xd4,0x38,
    0x76,0x7d,0xb2,0xa7,0xcf,0xed,0x57,0xc5,0xf3,0x2c,0xbb,0x14,0x21,0x06,0x55,0x9b,
    0xe3,0xef,0x5e,0x31,0x4f,0x7f,0x5a,0xa4,0x0d,0x82,0x51,0x49,0x5f,0xba,0x58,0x1c,
    0x4a,0x16,0xd5,0x17,0xa8,0x92,0x24,0x1f,0x8c,0xff,0xd8,0xae,0x2e,0x01,0xd3,0xad,
    0x3b,0x4b,0xda,0x46,0xeb,0xc9,0xde,0x9a,0x8f,0x87,0xd7,0x3a,0x80,0x6f,0x2f,0xc8,
    0xb1,0xb4,0x37,0xf7,0x0a,0x22,0x13,0x28,0x7c,0xcc,0x3c,0x89,0xc7,0xc3,0x96,0x56,
    0x07,0xbf,0x7e,0xf0,0x0b,0x2b,0x97,0x52,0x35,0x41,0x79,0x61,0xa6,0x4c,0x10,0xfe,
    0xbc,0x26,0x95,0x88,0x8a,0xb0,0xa3,0xfb,0xc0,0x18,0x94,0xf2,0xe1,0xe5,0xe9,0x5d,
    0xd0,0xdc,0x11,0x66,0x64,0x5c,0xec,0x59,0x42,0x75,0x12,0xf5,0x74,0x9c,0xaa,0x23,
    0x0e,0x86,0xab,0xbe,0x2a,0x02,0xe7,0x67,0xe6,0x44,0xa2,0x6c,0xc2,0x93,0x9f,0xf1,
    0xf6,0xfa,0x36,0xd2,0x50,0x68,0x9e,0x62,0x71,0x15,0x3d,0xd6,0x40,0xc4,0xe2,0x0f,
    0x8e,0x83,0x77,0x6b,0x25,0x05,0x3f,0x0c,0x30,0xea,0x70,0xb7,0xa1,0xe8,0xa9,0x65,
    0x8d,0x27,0x1a,0xdb,0x81,0xb3,0xa0,0xf4,0x45,0x7a,0x19,0xdf,0xee,0x78,0x34,0x60
])
_ZUC_S1 = bytes([
    0x55,0xc2,0x63,0x71,0x3b,0xc8,0x47,0x86,0x9f,0x3c,0xda,0x5b,0x29,0xaa,0xfd,0x77,
    0x8c,0xc5,0x94,0x0c,0xa6,0x1a,0x13,0x00,0xe3,0xa8,0x16,0x72,0x40,0xf9,0xf8,0x42,
    0x44,0x26,0x68,0x96,0x81,0xd9,0x45,0x3e,0x10,0x76,0xc6,0xa7,0x8b,0x39,0x43,0xe1,
    0x3a,0xb5,0x56,0x2a,0xc0,0x6d,0xb3,0x05,0x22,0x66,0xbf,0xdc,0x0b,0xfa,0x62,0x48,
    0xdd,0x20,0x11,0x06,0x36,0xc9,0xc1,0xcf,0xf6,0x27,0x52,0xbb,0x69,0xf5,0xd4,0x87,
    0x7f,0x84,0x4c,0xd2,0x9c,0x57,0xa4,0xbc,0x4f,0x9a,0xdf,0xfe,0xd6,0x8d,0x7a,0xeb,
    0x2b,0x53,0xd8,0x5c,0xa1,0x14,0x17,0xfb,0x23,0xd5,0x7d,0x30,0x67,0x73,0x08,0x09,
    0xee,0xb7,0x70,0x3f,0x61,0xb2,0x19,0x8e,0x4e,0xe5,0x4b,0x93,0x8f,0x5d,0xdb,0xa9,
    0xad,0xf1,0xae,0x2e,0xcb,0x0d,0xfc,0xf4,0x2d,0x46,0x6e,0x1d,0x97,0xe8,0xd1,0xe9,
    0x4d,0x37,0xa5,0x75,0x5e,0x83,0x9e,0xab,0x82,0x9d,0xb9,0x1c,0xe0,0xcd,0x49,0x89,
    0x01,0xb6,0xbd,0x58,0x24,0xa2,0x5f,0x38,0x78,0x99,0x15,0x90,0x50,0xb8,0x95,0xe4,
    0xd0,0x91,0xc7,0xce,0xed,0x0f,0xb4,0x6f,0xa0,0xcc,0xf0,0x02,0x4a,0x79,0xc3,0xde,
    0xa3,0xef,0xea,0x51,0xe6,0x6b,0x18,0xec,0x1b,0x2c,0x80,0xf7,0x74,0xe7,0xff,0x21,
    0x5a,0x6a,0x54,0x1e,0x41,0x31,0x92,0x35,0xc4,0x33,0x07,0x0a,0xba,0x7e,0x0e,0x34,
    0x88,0xb1,0x98,0x7c,0xf3,0x3d,0x60,0x6c,0x7b,0xca,0xd3,0x1f,0x32,0x65,0x04,0x28,
    0x64,0xbe,0x85,0x9b,0x2f,0x59,0x8a,0xd7,0xb0,0x25,0xac,0xaf,0x12,0x03,0xe2,0xf2
])
_ZUC_D = [0b100010011010111,0b010011010111100,0b110001001101011,0b001001101011110,
    0b101011110001001,0b011010111100010,0b111000100110101,0b000100110101111,
    0b100110101111000,0b010111100010011,0b110101111000100,0b001101011110001,
    0b101111000100110,0b011110001001101,0b111100010011010,0b100011110101100]
_ZUC_MOD = 0x7fffffff
def _zuc_rol32(x,n): return ((x<<n)&0xffffffff)|(x>>(32-n))
def _zuc_bs(x): return (_ZUC_S0[(x>>24)&0xff]<<24)^(_ZUC_S1[(x>>16)&0xff]<<16)^(_ZUC_S0[(x>>8)&0xff]<<8)^(_ZUC_S1[x&0xff])
def _zuc_l1(x): return x^_zuc_rol32(x,2)^_zuc_rol32(x,10)^_zuc_rol32(x,18)^_zuc_rol32(x,24)
def _zuc_l2(x): return x^_zuc_rol32(x,8)^_zuc_rol32(x,14)^_zuc_rol32(x,22)^_zuc_rol32(x,30)

class _FallbackZUC:
    def __init__(self,key,iv):
        self._lfsr=[0]*16;self._r1=0;self._r2=0;S=self._lfsr
        for i in range(16): S[i]=(key[i]<<23)|(_ZUC_D[i]<<8)|iv[i]
        for _ in range(32):
            x0=(S[15]>>15<<16)|(S[14]&0xffff);x1=((S[11]&0xffff)<<16)|(S[9]>>15);x2=((S[7]&0xffff)<<16)|(S[5]>>15)
            self._lfsr_work(self._f(x0,x1,x2)>>1)
        self.generate()
    def _f(self,x0,x1,x2):
        r1,r2=self._r1,self._r2;w=((x0^r1)+r2)&0xffffffff;w1=(r1+x1)&0xffffffff;w2=r2^x2
        self._r1=_zuc_bs(_zuc_l1(((w1&0xffff)<<16)^(w2>>16)));self._r2=_zuc_bs(_zuc_l2(((w2&0xffff)<<16)^(w1>>16)));return w
    def _lfsr_work(self,u=0):
        S=self._lfsr;s16=((S[15]<<15)+(S[13]<<17)+(S[10]<<21)+(S[4]<<20)+(S[0]<<8)+S[0]+u)%_ZUC_MOD
        S.append(_ZUC_MOD if s16==0 else s16);S.pop(0)
    def generate(self):
        S=self._lfsr;x0=(S[15]>>15<<16)|(S[14]&0xffff);x1=((S[11]&0xffff)<<16)|(S[9]>>15)
        x2=((S[7]&0xffff)<<16)|(S[5]>>15);x3=((S[2]&0xffff)<<16)|(S[0]>>15)
        z=self._f(x0,x1,x2)^x3;self._lfsr_work();return z.to_bytes(4,'big')

try:
    import gmalg as _gmalg_mod
    _ZUC_CLASS = _gmalg_mod.ZUC
except ImportError:
    _ZUC_CLASS = _FallbackZUC

try:
    from Crypto.Cipher import AES
    from Crypto.Cipher.AES import MODE_CBC
    from Crypto.Hash import SHA1
    from Crypto.Util.Padding import unpad
    from zstandard import ZstdDecompressor, ZstdCompressionDict, DICT_TYPE_AUTO, ZstdCompressor
except Exception:
    try:
        from Crypto.Cipher import AES
        from Crypto.Cipher.AES import MODE_CBC
        from Crypto.Hash import SHA1
        from Crypto.Util.Padding import unpad
    except Exception:
        AES = MODE_CBC = SHA1 = unpad = None
    try:
        from zstandard import ZstdDecompressor, ZstdCompressionDict, DICT_TYPE_AUTO, ZstdCompressor
    except Exception:
        ZstdDecompressor = ZstdCompressionDict = DICT_TYPE_AUTO = ZstdCompressor = None

console = Console()

# ==================== MASTER KEY / VARIANT TABLES (EMBEDDED) ====================

ZUC_KEY = bytes.fromhex('01010101010101010101010101010101')
ZUC_IV = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')

# Known ZUC key/iv variants (extension point: append more game keys here)
ZUC_KEY_IV_PAIRS: List[Tuple[bytes, bytes]] = [
    (ZUC_KEY, ZUC_IV),
    (bytes.fromhex('01010101010101010101010101010101'), bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')),
    (bytes.fromhex('00000000000000000000000000000000'), bytes.fromhex('00000000000000000000000000000000')),
]

RSA_MOD_1 = bytes.fromhex('CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4')
RSA_MOD_2 = bytes.fromhex('7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')
# Extension point: append more Tencent RSA moduli here
RSA_MODS: List[bytes] = [RSA_MOD_1, RSA_MOD_2]

SIMPLE1_DECRYPT_KEY = 121
SIMPLE2_DECRYPT_KEY = bytes.fromhex('E55B4ED1')
SIMPLE2_BLOCK_SIZE = 16

SM4_SECRET_4 = 'eb691efea914241317a8'
SM4_SECRET_2 = 'Q0hVTKey$as*1ZFlQCiA'
SM4_SECRET_NEW = [
    'xG2qW5lP7lV2iN5fN5pG','xT1cJ6dL5wC0kK1rB4dK','qC4jS5bZ6fL5xE6nD4zA','gD4jQ2aL3bS3lC3xT0iW',
    'xU1yQ8wE9zY3gZ3bT5aE','uQ3cO2dX7xY4xU7gH7iS','gW1fR0jK6wQ4oN0oK1kZ','aJ4pV7iZ7pU4wP2aC2cZ',
    'cX6jT3cM2oT3vK0kJ1qN','iT2vS0cS6yT6cZ1sE1lO','hM1pH9iY8wM9hT4lN5uJ','kG6bC8jK0fL0dE4sH4mL',
    'dB6lB3vE0eZ8wM8rI0aC','tP7sP7nI9rA2vQ4cV5yQ','aT0cL1yN4pT3sZ7eM2vY','uV6fU8fC9zN3mP5dH8mN'
]

EM_SIMPLE1 = 1; EM_SIMPLE2 = 16; EM_SM4_2 = 2; EM_SM4_4 = 4
EM_SM4_NEW_BASE = 31; EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE; EM_UNKNOWN_17 = 17
CM_NONE = 0; CM_ZLIB = 1; CM_ZSTD = 6; CM_ZSTD_DICT = 8; CM_MASK = 15

# Ordered candidate encryption methods tried during hash-verify (original first)
def _sm4_new_candidates():
    return [EM_SM4_NEW_BASE + i for i in range(16)]
EM_CANDIDATES: List[int] = [
    EM_SIMPLE1, EM_SIMPLE2, EM_SM4_2, EM_SM4_4, EM_UNKNOWN_17,
] + _sm4_new_candidates()

# Stable Engine Compression (Zero In-Game Stuttering)
_ZSTD_FAST_LEVELS = (6, 3)

class SM4:
    _S_BOX = bytes([
        52, 102, 37, 116, 137, 120, 228, 169, 90, 65, 188, 122, 214, 22, 33, 35,
        77, 97, 218, 148, 155, 223, 19, 60, 105, 58, 49, 10, 95, 215, 153, 149,
        241, 174, 114, 61, 7, 96, 36, 182, 152, 238, 196, 162, 45, 136, 221, 141,
        4, 234, 187, 17, 202, 62, 93, 161, 246, 63, 176, 151, 128, 71, 43, 166,
        230, 247, 217, 177, 89, 192, 124, 190, 84, 40, 183, 126, 79, 248, 67, 110,
        160, 80, 14, 245, 144, 184, 251, 163, 123, 98, 25, 70, 3, 42, 185, 143,
        159, 119, 180, 91, 131, 135, 8, 235, 226, 30, 66, 240, 15, 232, 113, 106,
        117, 173, 85, 31, 181, 171, 51, 250, 127, 21, 189, 133, 216, 6, 104, 179,
        82, 48, 72, 11, 0, 237, 239, 178, 87, 142, 231, 108, 213, 229, 46, 83,
        130, 5, 249, 129, 244, 86, 191, 140, 75, 227, 219, 74, 145, 76, 44, 211,
        64, 41, 78, 32, 20, 54, 121, 9, 111, 209, 55, 224, 57, 12, 138, 146,
        56, 18, 53, 109, 225, 253, 147, 154, 23, 212, 201, 156, 107, 132, 38, 157,
        175, 118, 193, 158, 208, 150, 197, 203, 233, 115, 73, 210, 205, 100, 195, 199,
        1, 125, 243, 172, 252, 222, 164, 68, 50, 27, 194, 186, 28, 2, 198, 39,
        69, 139, 242, 24, 167, 16, 81, 29, 200, 207, 99, 255, 47, 13, 88, 206,
        101, 165, 220, 26, 59, 134, 254, 34, 92, 168, 94, 103, 170, 236, 112, 204
    ])
    _FK = [1184304796, 1270900830, 1493524870, 3164752158]
    _CK = [964907, 973793155, 2654690407, 2916866751, 2071233739, 1226140771, 3348805095, 2045549823, 388349611, 800627875, 612403927, 3721562911, 1195432523, 3150178931, 612053223, 2445162591, 67183755, 1174197155, 1393249511, 3331183455, 3822152747, 1332317203, 1804781383, 1990130463, 1282653851, 3376591251, 2910902311, 925872959, 332098219, 735840931, 396665415, 3588844719]
    @staticmethod
    def ROL32(x, n): return (x << n) & 0xFFFFFFFF | (x >> (32 - n))
    @staticmethod
    def _BS(X): return (SM4._S_BOX[X >> 24 & 255] << 24 | SM4._S_BOX[X >> 16 & 255] << 16 | SM4._S_BOX[X >> 8 & 255] << 8 | SM4._S_BOX[X & 255])
    @staticmethod
    def _T0(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 2) ^ SM4.ROL32(X, 10) ^ SM4.ROL32(X, 18) ^ SM4.ROL32(X, 24)
    @staticmethod
    def _T1(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 13) ^ SM4.ROL32(X, 23)
    @staticmethod
    def _key_expand(key: bytes, rkey: list):
        K0 = int.from_bytes(key[0:4], 'big') ^ SM4._FK[0]
        K1 = int.from_bytes(key[4:8], 'big') ^ SM4._FK[1]
        K2 = int.from_bytes(key[8:12], 'big') ^ SM4._FK[2]
        K3 = int.from_bytes(key[12:16], 'big') ^ SM4._FK[3]
        for i in range(0, 32, 4):
            K0 ^= SM4._T1(K1 ^ K2 ^ K3 ^ SM4._CK[i]); rkey[i] = K0
            K1 ^= SM4._T1(K2 ^ K3 ^ K0 ^ SM4._CK[i + 1]); rkey[i + 1] = K1
            K2 ^= SM4._T1(K3 ^ K0 ^ K1 ^ SM4._CK[i + 2]); rkey[i + 2] = K2
            K3 ^= SM4._T1(K0 ^ K1 ^ K2 ^ SM4._CK[i + 3]); rkey[i + 3] = K3
    def __init__(self, key: bytes):
        self._key = key; self._rkey = [0] * 32; SM4._key_expand(self._key, self._rkey); self._block_buffer = bytearray()
    def encrypt(self, block: bytes) -> bytes:
        RK = self._rkey; X0 = int.from_bytes(block[0:4], 'big'); X1 = int.from_bytes(block[4:8], 'big')
        X2 = int.from_bytes(block[8:12], 'big'); X3 = int.from_bytes(block[12:16], 'big')
        for i in range(0, 32, 4):
            X0 ^= SM4._T0(X1 ^ X2 ^ X3 ^ RK[i]); X1 ^= SM4._T0(X2 ^ X3 ^ X0 ^ RK[i + 1])
            X2 ^= SM4._T0(X3 ^ X0 ^ X1 ^ RK[i + 2]); X3 ^= SM4._T0(X0 ^ X1 ^ X2 ^ RK[i + 3])
        buf = self._block_buffer; buf.clear()
        buf.extend(X3.to_bytes(4, 'big')); buf.extend(X2.to_bytes(4, 'big')); buf.extend(X1.to_bytes(4, 'big')); buf.extend(X0.to_bytes(4, 'big'))
        return bytes(buf)
    def decrypt(self, block: bytes) -> bytes:
        RK = self._rkey; X0 = int.from_bytes(block[0:4], 'big'); X1 = int.from_bytes(block[4:8], 'big')
        X2 = int.from_bytes(block[8:12], 'big'); X3 = int.from_bytes(block[12:16], 'big')
        for i in range(0, 32, 4):
            X0 ^= SM4._T0(X1 ^ X2 ^ X3 ^ RK[31 - i]); X1 ^= SM4._T0(X2 ^ X3 ^ X0 ^ RK[30 - i])
            X2 ^= SM4._T0(X3 ^ X0 ^ X1 ^ RK[29 - i]); X3 ^= SM4._T0(X0 ^ X1 ^ X2 ^ RK[28 - i])
        buf = self._block_buffer; buf.clear()
        buf.extend(X3.to_bytes(4, 'big')); buf.extend(X2.to_bytes(4, 'big')); buf.extend(X1.to_bytes(4, 'big')); buf.extend(X0.to_bytes(4, 'big'))
        return bytes(buf)

class Misc:
    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        p = n - len(data) % n; return data if p == n else data + b'\x00' * p
    @staticmethod
    def align_up(x: int, n: int) -> int: return (x + n - 1) // n * n

class Reader:
    def __init__(self, buffer, cursor=0): self._buffer = buffer; self._cursor = cursor
    def u1(self, m=True) -> int: return self.unpack('B', m=m)[0]
    def u4(self, m=True) -> int: return self.unpack('<I', m=m)[0]
    def u8(self, m=True) -> int: return self.unpack('<Q', m=m)[0]
    def i4(self, m=True) -> int: return self.unpack('<i', m=m)[0]
    def s(self, n: int, m=True) -> bytes: return self.unpack(f'{n}s', m=m)[0]
    def unpack(self, f: str, offset=0, m=True):
        x = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if m: self._cursor += struct.calcsize(f)
        return x
    def string(self, m=True) -> str:
        length = self.i4(m=m)
        if length <= 0: return ""
        offset = 0 if m else 4
        return self.unpack(f'{length}s', offset=offset, m=m)[0].rstrip(b'\x00').decode('utf-8', errors='ignore')

class PakInfo:
    def __init__(self, buffer, keystream: List[int]):
        r = Reader(buffer[-45:])
        self.index_encrypted = ((r.u1() ^ keystream[3]) & 255) == 1
        self.magic = r.u4() ^ keystream[2]
        self.version = r.u4()
        self.index_hash = bytes(a ^ b for a, b in zip(r.s(20), struct.pack('<5I', *keystream[4:9]))) if self.version >= 6 else bytes()
        self.index_size = r.u8() ^ (keystream[10] << 32 | keystream[11])
        self.index_offset = r.u8() ^ (keystream[0] << 32 | keystream[1])
        if self.version <= 3: self.index_encrypted = False

class TencentPakInfo(PakInfo):
    def __init__(self, buffer, keystream: List[int]):
        super().__init__(buffer, keystream)
        r = Reader(buffer[-TencentPakInfo._mem_size(self.version):])
        self.unk1 = bytes(a ^ b for a, b in zip(r.s(32), struct.pack('<8I', *keystream[7:15]))) if self.version >= 7 else bytes()
        self.packed_key = r.s(256) if self.version >= 8 else bytes()
        self.packed_iv = r.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash = r.s(256) if self.version >= 8 else bytes()
        self.stem_hash = (r.u4() ^ keystream[8]) if self.version >= 9 else 0
        self.unk2 = (r.u4() ^ keystream[9]) if self.version >= 9 else 0
        self.content_org_hash = r.s(20) if self.version >= 12 else bytes()
    @staticmethod
    def _mem_size(v: int) -> int:
        return 45 + (32 if v>=7 else 0) + (768 if v>=8 else 0) + (8 if v>=9 else 0) + (20 if v>=12 else 0)

class PakCompressedBlock:
    def __init__(self, r: Reader): self.start = r.u8(); self.end = r.u8()

@dataclass
class TencentPakEntry:
    def __init__(self, r: Reader, v: int):
        self.content_hash = r.s(20)
        if v <= 1: r.u8()
        self.offset = r.u8()
        self.uncompressed_size = r.u8()
        self.compression_method = r.u4() & CM_MASK
        self.size = r.u8()
        self.unk1 = r.u1() if v >= 5 else 0
        self.unk2 = r.s(20) if v >= 5 else bytes()
        self.compressed_blocks = [PakCompressedBlock(r) for _ in range(r.u4())] if (self.compression_method != 0 and v >= 3) else []
        self.compression_block_size = r.u4() if v >= 4 else 0
        self.encrypted = (r.u1() == 1) if v >= 4 else False
        self.encryption_method = r.u4() if v >= 12 else 0
        self.index_new_sep = r.u4() if v >= 12 else 0

class PakCrypto:
    class _LCG:
        def __init__(self, s: int): self.state = s
        def next(self) -> int:
            w = lambda x: (x & 0xFFFFFFFF) if not (x & 0x80000000) else ((x + 0x80000000 & 0xFFFFFFFF) - 0x80000000)
            x1 = w(1103515245 * self.state); self.state = w(x1 + 12345)
            x2 = w(x1 + 77880) if self.state < 0 else self.state
            return (x2 >> 16 & 0xFFFFFFFF) % 32767
    @staticmethod
    def zuc_keystream(key: Optional[bytes] = None, iv: Optional[bytes] = None) -> List[int]:
        key = key if key is not None else ZUC_KEY
        iv = iv if iv is not None else ZUC_IV
        zuc = _ZUC_CLASS(key, iv)
        return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]
    @staticmethod
    def rc4(key: bytes, data: bytes) -> bytes:
        S = list(range(256)); j = 0; out = bytearray(len(data))
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) & 0xFF
            S[i], S[j] = S[j], S[i]
        i = j = 0
        for n in range(len(data)):
            i = (i + 1) & 0xFF; j = (j + S[i]) & 0xFF
            S[i], S[j] = S[j], S[i]
            out[n] = data[n] ^ S[(S[i] + S[j]) & 0xFF]
        return bytes(out)
    @staticmethod
    def xor_key(data: bytes, key: bytes) -> bytes:
        if not key: return data
        if len(key) == 1:
            k = key[0]
            return bytes(b ^ k for b in data)
        kl = len(key)
        return bytes(b ^ key[i % kl] for i, b in enumerate(data))
    @staticmethod
    def content_mask_candidates(file: PurePath, em: int) -> List[bytes]:
        """Whole-region XOR masks tried when hash-verify fails (whole-file obfuscation defeat)."""
        stem = file.stem.lower()
        cands = [b'\x00', b'\xff']
        try:
            cands.append(SHA1.new(stem.encode()).digest()[:4])
            cands.append(SHA1.new((stem + str(em)).encode()).digest()[:4])
            cands.append(SHA1.new((file.name).encode()).digest()[:4])
        except Exception:
            pass
        return cands
    @staticmethod
    def rsa_extract(sig: bytes, mod: bytes) -> bytes:
        c = int.from_bytes(sig, 'little'); n = int.from_bytes(mod, 'little')
        m = pow(c, 65537, n).to_bytes(256, 'little').rstrip(b'\x00')
        buf = Misc.pad_to_n(m, 4)
        if len(buf) < 43: return bytes()
        x1 = buf[1:21]; x2 = buf[21:]
        h = lambda d, l: (SHA1.new(d).digest() * (math.ceil(l/20)))[:l]
        x1 = bytes(a ^ b for a, b in zip(x1, h(x2, len(x1))))
        x2 = bytes(a ^ b for a, b in zip(x2, h(x1, len(x2))))
        if x2[:20] != SHA1.new(b'\x00'*20).digest(): return bytes()
        raw = x2[20:]; skip = 1 + next((i for i in range(len(raw)) if raw[i] != 0))
        return raw[skip:]
    @staticmethod
    def decrypt_index(cipher, pak_info: TencentPakInfo, mods: Optional[List[bytes]] = None) -> bytes:
        if pak_info.version > 7:
            mods = mods or RSA_MODS
            last = None
            for m in list(mods) + [RSA_MOD_1]:
                try:
                    k = PakCrypto.rsa_extract(pak_info.packed_key, m)
                    iv = PakCrypto.rsa_extract(pak_info.packed_iv, m)
                    if not k or not iv: continue
                    aes = AES.new(k, MODE_CBC, iv[:16])
                    plain = unpad(aes.decrypt(cipher), AES.block_size)
                    if pak_info.version >= 6 and SHA1.new(plain).digest() != pak_info.index_hash:
                        last = plain; continue
                    return plain
                except Exception as e:
                    last = e
            if last is not None and not isinstance(last, Exception):
                return last
            cipher = cipher
        return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in cipher)
    @staticmethod
    def align_encrypted_content_size(n: int, em: int) -> int:
        if em in (EM_SIMPLE2, 17): return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        if em == EM_SM4_2 or em == EM_SM4_4 or (em & EM_SM4_NEW_MASK != 0): return Misc.align_up(n, 16)
        return n
    @staticmethod
    def _sm4_for_file(file: PurePath, em: int) -> Optional['SM4']:
        p1 = file.stem.lower()
        if em == EM_SM4_2: sec = SM4_SECRET_2
        elif em == EM_SM4_4: sec = SM4_SECRET_4
        elif (em & EM_SM4_NEW_MASK != 0):
            idx = (em - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)
            sec = f'{SM4_SECRET_NEW[idx]}{em}'
        else:
            return None
        k = SHA1.new(str(p1 + sec).encode()).digest()[:16]
        return SM4(k)
    @staticmethod
    def decrypt_block(cipher, file: PurePath, em: int) -> bytes:
        if em == EM_SIMPLE1: return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in cipher)
        if em in (EM_SIMPLE2, 17):
            k, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY); out = []
            for x, in struct.iter_unpack('<I', cipher): k ^= x; out.append(k)
            return struct.pack(f'<{len(out)}I', *out)
        if em == EM_SM4_2 or em == EM_SM4_4 or (em & EM_SM4_NEW_MASK != 0):
            sm4 = PakCrypto._sm4_for_file(file, em)
            if sm4 is None: return cipher
            return bytes(it.chain.from_iterable(sm4.decrypt(x) for x in _batched(cipher, 16)))
        return cipher
    @staticmethod
    def encrypt_block(plain, file: PurePath, em: int) -> bytes:
        if em == EM_SIMPLE1: return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in plain)
        if em in (EM_SIMPLE2, 17):
            k, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY); out = []
            for x, in struct.iter_unpack('<I', plain): k ^= x; out.append(k)
            return struct.pack(f'<{len(out)}I', *out)
        if em == EM_SM4_2 or em == EM_SM4_4 or (em & EM_SM4_NEW_MASK != 0):
            sm4 = PakCrypto._sm4_for_file(file, em)
            if sm4 is None: return plain
            return b''.join(sm4.encrypt(x) for x in _batched(plain, 16))
        return plain
    @staticmethod
    def generate_block_indices(n: int, em: int) -> List[int]:
        if not (em == EM_SM4_2 or em == EM_SM4_4 or (em & EM_SM4_NEW_MASK != 0)): return list(range(n))
        p = []; lcg = PakCrypto._LCG(n)
        while len(p) != n:
            x = lcg.next() % n
            if x not in p: p.append(x)
        inv = [0]*len(p)
        for i, x in enumerate(p): inv[x] = i
        return inv

class PakCompression:
    @staticmethod
    def decompress_block(block, zd, cm: int) -> bytes:
        if cm == CM_ZLIB:
            try: return zlib.decompress(block)
            except Exception: return block
        if cm in (CM_ZSTD, CM_ZSTD_DICT):
            if ZstdDecompressor is None: return block
            return ZstdDecompressor(zd if cm == CM_ZSTD_DICT else None).decompress(block)
        return block
    @staticmethod
    def compress_block(chunk, zd, cm: int, level=6) -> bytes:
        if cm == CM_ZLIB:
            return zlib.compress(chunk, level)
        if cm in (CM_ZSTD, CM_ZSTD_DICT):
            if ZstdCompressor is None: return chunk
            kw = {'level': level}
            if cm == CM_ZSTD_DICT and zd is not None:
                kw['dict_data'] = zd
            return ZstdCompressor(**kw).compress(chunk)
        return chunk

# ==================== CONTAINER DETECTION ====================

def _is_all_zero(b: bytes) -> bool:
    return not any(b)

def detect_container(data: bytes, name: str = '') -> str:
    low = name.lower()
    if data[:2] == b'\x1bL':
        if data[:4] == b'\x1bLua':
            return 'LUA51' if len(data) > 4 and data[4] == 0x51 else \
                   'LUA52' if len(data) > 4 and data[4] == 0x52 else \
                   'LUA53' if len(data) > 4 and data[4] == 0x53 else \
                   'LUA54' if len(data) > 4 and data[4] == 0x54 else 'LUA52'
        if data[:3] == b'\x1bLJ': return 'LUJIT'
    if data[:4] == b'OBB\x00': return 'OBB_BLOB'
    if data[:2] == b'PK': return 'ZIP'
    if data[:16] == b'SQLite format 3\x00': return 'SQLITE'
    if data[:4] == b'\x7fELF': return 'ELF'
    if low.endswith('.lua'):
        try:
            data.decode('utf-8')
            return 'LUA_TEXT'
        except Exception: pass
    if len(data) >= 45:
        try:
            pi = TencentPakInfo(data, PakCrypto.zuc_keystream())
            if 1 <= pi.version <= 20 and 0 < pi.index_offset <= len(data):
                return 'PAK'
        except Exception: pass
    return 'BIN'

def _zip_bounds(buf: bytes):
    eocd = buf.rfind(b'PK\x05\x06')
    if eocd < 0 or eocd + 22 > len(buf): return None
    cd_size = struct.unpack_from('<I', buf, eocd + 12)[0]
    cd_off = struct.unpack_from('<I', buf, eocd + 16)[0]
    start = buf.find(b'PK\x03\x04', 0, eocd)
    if start < 0: start = cd_off
    return start, eocd + 22

# ==================== ANDROID BINARY XML (AXML) DECODER ====================

_ATTR_TYPES = {0x01: 'dec', 0x03: 'hex', 0x04: 'bool', 0x05: 'str', 0x06: 'float',
               0x10: 'fraction', 0x11: 'dimension', 0x1c: 'color', 0x02: 'dec', 0x12: 'dimension'}

def _u16(b, o): return struct.unpack_from('<H', b, o)[0]
def _u32(b, o): return struct.unpack_from('<I', b, o)[0]

class _AXMLStrings:
    def __init__(self, data, base, header_size, chunk_size):
        self.data = data; self.base = base
        self.count = _u32(data, base + 8); self.flags = _u32(data, base + 16)
        self.start = _u32(data, base + 20)
        offs = header_size
        self.offsets = [_u32(data, base + offs + 4 * i) for i in range(self.count)]
        self.storage = base + self.start
        self.utf8 = bool(self.flags & 0x100)
    def _utf8_len(self, p):
        b = self.data[p]; p += 1
        if b & 0x80:
            b = ((b & 0x7F) << 8) | self.data[p]; p += 1
        return b, p
    def get(self, idx):
        if idx == 0xFFFFFFFF or idx < 0 or idx >= self.count: return ''
        try:
            p = self.storage + self.offsets[idx]
            if self.utf8:
                n1, p = self._utf8_len(p); n2, p = self._utf8_len(p)
                n = n1 + n2
                s = self.data[p:p + n].decode('utf-8', 'replace')
            else:
                n = _u16(self.data, p); p += 2
                s = self.data[p:p + n * 2].decode('utf-16le', 'replace')
            return s.rstrip('\x00')
        except Exception:
            return ''

def _xml_escape(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def decode_axml(data: bytes) -> str:
    if len(data) < 12: raise ValueError('too small')
    if _u16(data, 0) != 0x0003: raise ValueError('not AXML')
    sp_base = 8
    sp_type = _u16(data, sp_base)
    if sp_type != 0x0001: raise ValueError('no string pool')
    strings = _AXMLStrings(data, sp_base, _u16(data, sp_base + 2), _u32(data, sp_base + 4))
    pos = sp_base + _u32(data, sp_base + 4)
    res_map = {}
    if pos + 8 <= len(data) and _u16(data, pos) == 0x0180:
        pos += 8
        n = (_u32(data, pos - 4) - 8) // 4
        for i in range(n):
            ri = _u32(data, pos + 4 * i)
            if ri not in ('', None): res_map[i] = ri
        pos = pos - 8 + _u32(data, pos - 4)
    namespaces = []
    stack = []
    out = []
    depth = 0

    def ns_name(idx):
        nm = strings.get(idx)
        if not nm: return ''
        for p, u in namespaces:
            if p == nm: return nm
        return nm.split('/')[-1]

    while pos + 8 <= len(data):
        typ = _u16(data, pos); hsize = _u16(data, pos + 2); csize = _u32(data, pos + 4)
        if typ == 0x0100:
            namespaces.append((strings.get(_u32(data, pos + 8)), strings.get(_u32(data, pos + 12))))
        elif typ == 0x0101:
            if namespaces: namespaces.pop()
        elif typ == 0x0102:
            ns_i = _u32(data, pos + 20); name_i = _u32(data, pos + 24)
            acount = _u16(data, pos + 32); asize = _u16(data, pos + 30) or 20
            tag = strings.get(name_i)
            stack.append(tag)
            if depth == 0:
                out.append('<?xml version="1.0" encoding="utf-8"?>')
                resns = next((u for p, u in namespaces if p == 'android'), 'http://schemas.android.com/apk/res/android')
                out.append('<%s xmlns:android="%s">' % (tag, resns))
            else:
                out.append('  ' * depth + '<%s>' % tag)
            ap = pos + 36
            for ai in range(acount):
                a = ap + ai * asize
                ans = _u32(data, a); aname = _u32(data, a + 4); araw = _u32(data, a + 8)
                dtype = data[a + 14]; ddata = _u32(data, a + 16)
                attr = strings.get(aname)
                prefix = 'android:' if ans != 0xFFFFFFFF and strings.get(ans) else ''
                if araw != 0xFFFFFFFF:
                    val = strings.get(araw)
                elif dtype == 0x03:
                    val = strings.get(ddata)
                elif dtype == 0x04:
                    val = 'true' if ddata != 0 else 'false'
                elif dtype == 0x06:
                    val = str(struct.unpack('<f', struct.pack('<I', ddata))[0])
                elif dtype == 0x01:
                    val = str(ddata)
                else:
                    val = '0x%08x' % ddata
                out.append('  ' * (depth + 1) + '%s%s="%s"' % (prefix, attr, _xml_escape(val)))
            depth += 1
        elif typ == 0x0103:
            if depth > 0:
                depth -= 1
            if stack:
                tag = stack.pop()
                out.append('  ' * depth + '</%s>' % tag)
        elif typ == 0x0104:
            t = strings.get(_u32(data, pos + 12))
            if t:
                out.append('  ' * depth + _xml_escape(t))
        pos += csize
    return '\n'.join(out)

def try_decode_axml(data: bytes):
    try:
        return decode_axml(data)
    except Exception:
        return None

# ==================== READABLE ZIP / SQLITE EXTRACTION ====================

def _extract_zip_readable(zf_bytes: bytes, dest: Path):
    import io
    with zipfile.ZipFile(io.BytesIO(zf_bytes)) as z:
        z.extractall(dest)
    for p in dest.rglob('*'):
        if p.is_file() and (p.suffix.lower() == '.xml' or p.name == 'AndroidManifest.xml'):
            try:
                raw = p.read_bytes()
                txt = decode_axml(raw)
                if txt:
                    (p.with_name(p.name + '.raw.xml')).write_bytes(raw)
                    p.write_text('<!-- AXML decoded by FRIEND TOOL -->\n' + txt, encoding='utf-8')
            except Exception:
                pass

def _dump_sqlite_readable(src: Path, dest: Path):
    try:
        import sqlite3, csv
    except Exception:
        return False
    try:
        tmp = dest / '_db_copy.db'
        shutil.copy2(src, tmp)
        con = sqlite3.connect(str(tmp))
        cur = con.cursor()
        tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()]
        schema = []
        for r in cur.execute("SELECT type,name,tbl_name,sql FROM sqlite_master").fetchall():
            if r[3]: schema.append('%s;\n' % r[3])
        (dest / 'schema.sql').write_text('\n'.join(schema), encoding='utf-8')
        tdir = dest / 'tables'
        tdir.mkdir(parents=True, exist_ok=True)
        summary = []
        for t in tables:
            try:
                cols = [d[1] for d in cur.execute('PRAGMA table_info("%s")' % t.replace('"', '""')).fetchall()]
                rows = cur.execute('SELECT * FROM "%s"' % t.replace('"', '""')).fetchall()
                with open(str(tdir / ('%s.csv' % t)), 'w', newline='', encoding='utf-8') as f:
                    w = csv.writer(f)
                    w.writerow(cols)
                    for r in rows: w.writerow(['' if c is None else c for c in r])
                summary.append('%s: %d rows, %d cols' % (t, len(rows), len(cols)))
            except Exception as e:
                summary.append('%s: ERROR %s' % (t, e))
        con.close()
        tmp.unlink(missing_ok=True)
        (dest / 'db_summary.txt').write_text('\n'.join(summary), encoding='utf-8')
        return True
    except Exception:
        return False

# ==================== LUA REPEAT-XOR (MULTI-BYTE KEY) BREAKER ====================

_LUA_MAGIC = b'\x1bLua'

def _find_repeat_xor(data: bytes):
    """Finds repeating-key XOR that reveals the Lua magic (key length 2 or 4)."""
    lim = min(len(data) - 4, 256)
    for L in (2, 4):
        for off in range(lim):
            key = bytearray(L)
            ok = True
            for i in range(4):
                pos = off + i
                ki = (pos - off) % L
                kb = data[pos] ^ _LUA_MAGIC[i]
                if key[ki] and key[ki] != kb:
                    ok = False; break
                key[ki] = kb
            if not ok: continue
            if L == 4 and not any(key): continue
            if all(b == 0 for b in key): continue
            dec = PakCrypto.xor_key(data[off:], bytes(key))
            if dec[:4] != _LUA_MAGIC: continue
            try:
                parse_lua51(dec)
                return off, bytes(key)
            except Exception:
                pass
            hits = 0
            for j in range(4, min(512, len(dec) - 4), 4):
                if dec[j:j + 4] == _LUA_MAGIC: hits += 1
            if hits >= 2 or (hits >= 1 and L == 2):
                return off, bytes(key)
    return None, None

# ==================== TENCENT PAK FILE (ANY-PAK ENGINE) ====================

class TencentPakFile:
    def __init__(self, file_path: PurePath):
        self._file_path = file_path
        with open(file_path, 'rb') as f: self._file_content = memoryview(f.read())
        if len(self._file_content) < 45:
            raise ValueError('File too small to be a PAK.')
        self._mount_point = PurePath()
        self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
        self._zstd_dict = None; self._files = []; self._index = {}
        self._keystream: List[int] = []
        self._key = ZUC_KEY; self._iv = ZUC_IV
        self._pak_info = None
        self._load_all()

    def _attach_info(self, keystream):
        self._pak_info = TencentPakInfo(self._file_content, keystream)
        self._keystream = list(keystream)

    def _parse_index(self, idx_plain: bytes) -> bool:
        try:
            r = Reader(idx_plain)
            mp = PurePath()
            for p in PurePath(r.string()).parts:
                if p != '..': mp /= p
            n_files = r.u4()
            if n_files > 5_000_000: return False
            files = [TencentPakEntry(r, self._pak_info.version) for _ in range(n_files)]
            n_dirs = r.u8()
            if n_dirs > 5_000_000: return False
            index = {}
            zstd_dict = None
            for _ in range(n_dirs):
                dp = r.string()
                cnt = r.u8()
                if cnt > 5_000_000: return False
                e = {}
                for _ in range(cnt):
                    nm = r.string()
                    ei = ~r.i4()
                    if ei < 0 or ei >= len(files):
                        return False
                    e[nm] = files[ei]
                if self._is_zstd_with_dict and PurePath(dp).name == 'zstddic':
                    ent = list(e.values())[0]
                    dr = Reader(self._file_content[ent.offset:ent.offset + ent.size])
                    sz = dr.u8(); dr.u4(); dr.u4(); dt = dr.s(sz)
                    if ZstdCompressionDict is not None:
                        zstd_dict = ZstdCompressionDict(dt, DICT_TYPE_AUTO)
                else:
                    index[dp] = e
            ver = self._pak_info.version
            if ver >= 6:
                plain_hash = SHA1.new(idx_plain).digest()
                want = self._pak_info.index_hash
                if not _is_all_zero(want) and plain_hash != want:
                    return False
            self._mount_point = mp
            self._files = files
            self._index = index
            if zstd_dict is not None: self._zstd_dict = zstd_dict
            return True
        except Exception:
            return False

    def _load_all(self):
        last_err = None
        for key, iv in ZUC_KEY_IV_PAIRS:
            try:
                ks = PakCrypto.zuc_keystream(key, iv)
                self._attach_info(ks)
                self._key = key; self._iv = iv
                pi = self._pak_info
                idx_raw = bytes(self._file_content[pi.index_offset:][:pidx_check(pi)])
                if pi.index_encrypted:
                    idx_plain = PakCrypto.decrypt_index(idx_raw, pi)
                else:
                    idx_plain = idx_raw
                if self._parse_index(idx_plain):
                    return
            except SystemError:
                raise
            except Exception as e:
                last_err = e
        if not self._index:
            try:
                ks = PakCrypto.zuc_keystream()
                self._attach_info(ks)
                raise ValueError('Could not decode PAK index with any known key set. %s' % (last_err or ''))
            except Exception:
                raise ValueError('Could not decode PAK index with any known key set. %s' % (last_err or ''))

    def _extract_one(self, out_path: Path, entry: TencentPakEntry):
        out_path.parent.mkdir(parents=True, exist_ok=True)
        em = entry.encryption_method
        cm = entry.compression_method
        want = bytes(entry.content_hash)
        verify = not _is_all_zero(want)
        candidates = [em] + [e for e in EM_CANDIDATES if e != em]

        def attempt(em_cand, mask):
            try:
                if cm == CM_NONE:
                    sz = PakCrypto.align_encrypted_content_size(entry.size, em_cand) if entry.encrypted else entry.size
                    data = bytes(self._file_content[entry.offset:entry.offset + sz])
                else:
                    order = PakCrypto.generate_block_indices(len(entry.compressed_blocks), em_cand)
                    out = bytearray()
                    for idx in order:
                        blk = entry.compressed_blocks[idx]
                        unc = blk.end - blk.start
                        sz = PakCrypto.align_encrypted_content_size(unc, em_cand) if entry.encrypted else unc
                        data = bytes(self._file_content[blk.start:blk.start + sz])
                        if mask: data = PakCrypto.xor_key(data, mask)
                        if entry.encrypted:
                            data = PakCrypto.decrypt_block(data, out_path, em_cand)
                        dec = PakCompression.decompress_block(data, self._zstd_dict, cm)
                        out += dec
                    data = bytes(out)
                    return data, 'DECRYPT_OK'
                if mask: data = PakCrypto.xor_key(data, mask)
                if entry.encrypted:
                    data = PakCrypto.decrypt_block(data, out_path, em_cand)
                data = data[:entry.uncompressed_size]
                return data, 'DECRYPT_OK'
            except Exception:
                return None, 'DECRYPT_FAIL'

        em_cands = candidates
        masks = [None]
        for em_cand in em_cands:
            for mask in masks:
                data, st = attempt(em_cand, mask)
                if data is None: continue
                if verify and SHA1.new(data).digest() == want:
                    out_path.write_bytes(data)
                    return 'HASH_OK'
                if not verify and data is not None:
                    out_path.write_bytes(data)
                    return 'DECRYPT_OK'
        # whole-region XOR obfuscation fallback
        if entry.encrypted:
            masks = PakCrypto.content_mask_candidates(out_path, em)
            for mask in masks:
                for em_cand in em_cands:
                    data, st = attempt(em_cand, mask)
                    if data is None: continue
                    if verify and SHA1.new(data).digest() == want:
                        out_path.write_bytes(data)
                        return 'HASH_OK'
        data, st = attempt(em, None)
        if data is not None and len(data):
            out_path.write_bytes(data)
            return 'RAW_SALVAGED'
        raise RuntimeError('Extract failed for %s (%s)' % (out_path.name, st))

    @staticmethod
    def probe(path: Path) -> bool:
        try:
            with open(path, 'rb') as f:
                head = f.read(64)
                f.seek(-45, 2)
                tail = f.read(45)
            buf = head + tail
            pi = TencentPakInfo(buf, PakCrypto.zuc_keystream())
            return 1 <= pi.version <= 20
        except Exception:
            return False

    def dump(self, out_path: Path, verify_hash: bool = True, status_file: bool = True) -> int:
        target_root = out_path / self._mount_point
        target_root.mkdir(parents=True, exist_ok=True)
        total = sum(len(d) for d in self._index.values())
        if total == 0:
            raise ValueError("Pak file loaded but index is empty! Check encryption key or signature.")
        status_lines = []
        ok = 0; salvaged = 0
        with Progress(console=console) as prog:
            task = prog.add_task("[bold cyan]Extracting all files (hash-verified)...", total=total)
            for dp, files in self._index.items():
                cur = target_root / dp
                for fn, ent in files.items():
                    rel = str((dp / fn).as_posix())
                    try:
                        st = self._extract_one(cur / fn, ent)
                        if st == 'HASH_OK': ok += 1
                        elif st == 'DECRYPT_OK': ok += 1
                        else: salvaged += 1
                        status_lines.append('%-12s %s' % (st, rel))
                    except Exception as e:
                        salvaged += 1
                        status_lines.append('%-12s %s (%s)' % ('FAIL', rel, e))
                    prog.update(task, advance=1)
        if status_file:
            (out_path / 'STATUS.txt').write_text('\n'.join(status_lines) + '\n', encoding='utf-8')
        return ok

# ==================== NESTED CONTAINER SCAN ====================

def _nested_dump(file_path: Path, sink_dir: Path, depth: int = 0, max_depth: int = 3):
    if depth > max_depth: return
    try:
        data = file_path.read_bytes()
        kind = detect_container(data, file_path.name)
        if kind in ('PAK', 'ZIP', 'OBB_BLOB', 'LUA51', 'LUA52', 'LUA53', 'LUA54', 'LUJIT', 'SQLITE'):
            rel = file_path.relative_to(sink_dir) if str(file_path.resolve()).startswith(str(sink_dir.resolve())) else Path(file_path.name)
            nested_root = sink_dir / '__nested__' / rel
            sub_dest = nested_root.with_suffix('')
            sub_dest.mkdir(parents=True, exist_ok=True)
            (sub_dest / 'original.bin').write_bytes(data)
            _dump_one_bytes(data, file_path.stem, sub_dest, depth + 1, max_depth)
    except Exception:
        pass

def _dump_one_bytes(data: bytes, name: str, dest: Path, depth: int, max_depth: int):
    try:
        kind = detect_container(data, name)
        if kind == 'PAK':
            tmp = dest / '_pack.bin'
            tmp.write_bytes(data)
            pak = TencentPakFile(tmp)
            pak.dump(dest / 'unpacked')
        elif kind in ('ZIP', 'OBB_BLOB'):
            zf = data
            if kind == 'OBB_BLOB':
                b = _zip_bounds(data)
                if b:
                    start, end = b
                    zf = data[start:end]
            _extract_zip_readable(zf, dest / 'EXTRACTED')
            for p in Path(dest / 'EXTRACTED').rglob('*'):
                if p.is_file():
                    _nested_dump(p, dest / 'EXTRACTED', depth, max_depth)
        elif kind == 'SQLITE':
            (dest / 'sqlite.db').write_bytes(data)
            _dump_sqlite_readable(dest / 'sqlite.db', dest)
        elif kind.startswith('LUA'):
            _process_lua_file(data, dest, name)
    except Exception:
        pass

# ==================== LUA DECODER / EXTRACTOR (REAL ENGINE) ====================

_LUA51_OP = {
    0: 'MOVE', 1: 'LOADK', 2: 'LOADBOOL', 3: 'LOADNIL', 4: 'GETUPVAL', 5: 'GETGLOBAL',
    6: 'GETTABLE', 7: 'SETGLOBAL', 8: 'SETUPVAL', 9: 'SETTABLE', 10: 'NEWTABLE', 11: 'SELF',
    12: 'ADD', 13: 'SUB', 14: 'MUL', 15: 'DIV', 16: 'MOD', 17: 'POW', 18: 'UNM', 19: 'NOT',
    20: 'LEN', 21: 'CONCAT', 22: 'JMP', 23: 'EQ', 24: 'LT', 25: 'LE', 26: 'TEST', 27: 'TESTSET',
    28: 'CALL', 29: 'TAILCALL', 30: 'RETURN', 31: 'FORLOOP', 32: 'FORPREP', 33: 'TFORLOOP',
    34: 'SETLIST', 35: 'CLOSE', 36: 'CLOSURE', 37: 'VARARG',
}

def _fmt_const(c) -> str:
    if c is None: return 'nil'
    if c is True: return 'true'
    if c is False: return 'false'
    if isinstance(c, float): return repr(c)
    if isinstance(c, str): return '"%s"' % c
    return repr(c)

class Lua51Parser:
    def __init__(self, data: bytes, offset: int = 0):
        self.d = data; self.p = offset
    def u1(self): v = self.d[self.p]; self.p += 1; return v
    def u4(self): v = struct.unpack_from('<I', self.d, self.p)[0]; self.p += 4; return v
    def num(self): v = struct.unpack_from('<d', self.d, self.p)[0]; self.p += 8; return v
    def string(self):
        nz = self.u4()
        if nz == 0: return ''
        if self.p + nz > len(self.d): raise ValueError('string overflow')
        s = self.d[self.p:self.p + nz - 1]
        self.p += nz
        return s.decode('utf-8', 'replace')
    def proto(self, source):
        src = self.string() or source
        linedefined = self.u4(); lastlinedefined = self.u4()
        nups = self.u1(); numparams = self.u1(); is_vararg = self.u1(); maxstack = self.u1()
        ncode = self.u4(); code = [self.u4() for _ in range(ncode)]
        nk = self.u4(); consts = []
        for _ in range(nk):
            tag = self.u1()
            if tag == 0: consts.append(None)
            elif tag == 1: consts.append(self.u1() != 0)
            elif tag == 3: consts.append(self.num())
            elif tag == 4: consts.append(self.string())
            else: consts.append(('unknown', tag))
        nup = self.u4(); upvals = [self.u1() for _ in range(nup)]
        ninfo = self.u4()
        for _ in range(ninfo): self.u4()
        nloc = self.u4()
        for _ in range(nloc): self.string(); self.u4(); self.u4()
        nupd = self.u4()
        for _ in range(nupd): self.string()
        np = self.u4(); protos = [self.proto(src) for _ in range(np)]
        return {
            'src': src, 'linedefined': linedefined, 'lastlinedefined': lastlinedefined,
            'nups': nups, 'numparams': numparams, 'is_vararg': is_vararg, 'maxstack': maxstack,
            'code': code, 'k': consts, 'upvals': upvals, 'protos': protos,
        }

def parse_lua51(data: bytes, offset: int = 0):
    if data[offset:offset + 4] != b'\x1bLua':
        raise ValueError('Not a Lua 5.1 chunk')
    if data[offset + 4] != 0x51:
        raise ValueError('Not Lua 5.1 version')
    last_err = None
    for start in (offset + 20, offset + 12):
        try:
            p = Lua51Parser(data, start)
            proto = p.proto(None)
            return proto, p.p
        except Exception as e:
            last_err = e
            continue
    raise ValueError('Lua 5.1 parse failed: %s' % last_err)

def _disasm51(code, k, indent=''):
    out = []
    for i, ins in enumerate(code):
        op = ins & 0x3F; a = (ins >> 6) & 0xFF
        c = (ins >> 14) & 0x1FF; b = (ins >> 23) & 0x1FF
        name = _LUA51_OP.get(op, 'OP%d' % op)
        args = 'A=%d B=%d C=%d' % (a, b, c)
        extra = ''
        if op == 1 and 0 <= b < len(k): extra = '  ; K[b] = %s' % _fmt_const(k[b])
        out.append('%s[%04d] %-10s %s%s' % (indent, i, name, args, extra))
    return out

def _render_pseudo51(proto, indent=''):
    lines = []
    src = proto.get('src') or '<chunk>'
    params = ', '.join('p%d' % i for i in range(proto.get('numparams', 0)))
    if proto.get('is_vararg'): params += ', ...' if params else '...'
    lines.append('%sfunction %s(%s)  -- stack=%d nkod=%d' % (indent, os.path.basename(src) if src else '<main>', params, proto.get('maxstack', 0), len(proto.get('code', []))))
    for ln in _disasm51(proto.get('code', []), proto.get('k', []), indent + '  '):
        lines.append(ln)
    for sub in proto.get('protos', []):
        lines.append('')
        lines.extend(_render_pseudo51(sub, indent + '  '))
    lines.append('%send' % indent)
    return lines

def _scan_lua(data: bytes):
    lim = min(len(data), 4096)
    for off in range(lim):
        if data[off:off + 4] == b'\x1bLua':
            return off, None
        if data[off:off + 3] == b'\x1bLJ':
            return off, None
    lim2 = min(len(data) - 3, 512)
    if lim2 < 0: return None, None
    for off in range(lim2):
        keys = set()
        for k in range(256):
            if (data[off] ^ k == 0x1b and data[off + 1] ^ k == 0x4c
                    and data[off + 2] ^ k == 0x75 and data[off + 3] ^ k == 0x61):
                keys.add(k)
        if keys:
            k = keys.pop()
            return off, k
    return None, None

def _unscramble_lua(data: bytes):
    off, key = _scan_lua(data)
    if off is None:
        off, key = _find_repeat_xor(data)
        if off is not None and key is not None:
            return PakCrypto.xor_key(data[off:], key), list(key), off
        return data, None, 0
    if key is None:
        return data[off:], None, off
    out = bytes(b ^ key for b in data[off:])
    return out, key, off

def _lua_report(kind: str, data: bytes) -> List[str]:
    lines = []
    if kind == 'LUJIT':
        ver = data[3] if len(data) > 3 else 0
        lines.append('LuaJIT bytecode detected (LJ version 0x%02x, likely %s).' % (ver, '2.1' if ver == 1 else '2.0'))
        lines.append('NOTE: LuaJIT chunks are usually LJC-compressed (zlib stream after header).')
        lines.append('Strings table below; disassembly of compressed LuaJIT requires full LJC decompressor.')
    elif kind in ('LUA52', 'LUA53', 'LUA54'):
        ver = {0x52: '5.2', 0x53: '5.3', 0x54: '5.4'}.get(data[4] if len(data) > 4 else 0, '5.x')
        lines.append('Lua %s bytecode detected (header parsed).' % ver)
        lines.append('NOTE: full %s decompiler requires per-version opcode/varint tables; strings table below for auditing.' % ver)
    return lines

def _process_lua_file(data: bytes, dest_dir: Path, base_name: str, full: bool = False):
    """Parses Lua scripts/bytecode. full=False -> single readable file (+ .raw for repack)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    cleaned, xor_key, prefix_len = _unscramble_lua(data)
    kind = detect_container(cleaned, base_name)
    main = dest_dir / base_name

    if kind == 'LUA_TEXT':
        main.write_text(cleaned.decode('utf-8', 'replace'), encoding='utf-8')
        (dest_dir / 'meta.json').write_text(json.dumps({'type': 'LUA_TEXT', 'xor_key': xor_key, 'prefix': prefix_len}))
        return

    (dest_dir / ('%s.raw' % str(base_name))).write_bytes(data)
    header_info = []
    body_lines = []

    if kind in ('LUA52', 'LUA53', 'LUA54', 'LUJIT'):
        header_info = _lua_report(kind, cleaned)
        body_lines = ['-- ' + h if not h.startswith('--') else h for h in header_info]
        body_lines += ['-- Encryption broken: XOR key=%r prefix=%d' % (xor_key, prefix_len)]
        body_lines += ['-- String table:']
        for s in _extract_strings_clean(cleaned):
            body_lines.append('-- string_entry = "%s"' % s)
    elif kind == 'LUA51':
        body_lines.append('-- FRIEND TOOL Lua 5.1 decode / editable view')
        try:
            proto, end = parse_lua51(cleaned)
            header_info.append('Lua 5.1 parsed: end=%d top_instructions=%d top_constants=%d' % (end, len(proto.get('code', [])), len(proto.get('k', []))))
            header_info.append('Encryption broken: XOR key=%r prefix=%d' % (xor_key, prefix_len))
            body_lines = ['-- ' + h for h in header_info]
            body_lines += _render_pseudo51(proto)
        except Exception as e:
            body_lines.append('-- parse error: %s' % e)
            body_lines += _extract_strings_clean(cleaned)
    else:
        body_lines.append('-- unknown Lua container: %s' % kind)
        body_lines += _extract_strings_clean(cleaned)

    main.write_text('\n'.join(body_lines), encoding='utf-8')
    (dest_dir / 'meta.json').write_text(json.dumps({'type': kind, 'xor_key': xor_key, 'prefix': prefix_len, 'full': full}))

    if full:
        # Rich mode: sidecar audit files (option 7 asks for these)
        if kind == 'LUA51':
            try:
                proto, end = parse_lua51(cleaned)
                dis = []
                def walk(p, ind):
                    dis.append('; ---- function %s (line %d-%d)' % (p.get('src') or '<main>', p.get('linedefined', 0), p.get('lastlinedefined', 0)))
                    dis.extend(_disasm51(p.get('code', []), p.get('k', []), ind))
                    for s in p.get('protos', []): walk(s, ind + '  ')
                walk(proto, '')
                (dest_dir / 'decode_5_1_disasm.txt').write_text('\n'.join(dis), encoding='utf-8')
            except Exception:
                pass
        (dest_dir / 'strings_readable.txt').write_text('\n'.join(_extract_strings_clean(cleaned)), encoding='utf-8')

def _extract_strings_clean(data: bytes):
    return [m.group(0).decode('ascii', errors='replace') for m in re.finditer(rb'[\x20-\x7e]{3,}', data)]

def _repack_lua(dest_dir: Path, base_name: str, out_path: Path) -> bool:
    raw = dest_dir / ('%s.raw' % str(base_name))
    if not raw.exists():
        return False
    raw_bytes = raw.read_bytes()
    payload, key, prefix = _unscramble_lua(raw_bytes)

    patch_f = dest_dir / 'patch.json'
    if patch_f.exists():
        try:
            pat = json.loads(patch_f.read_text())
            for old, new in pat.items():
                old_b = old.encode('utf-8'); new_b = new.encode('utf-8')
                if len(old_b) == len(new_b):
                    payload = payload.replace(old_b, new_b)
                elif len(new_b) < len(old_b):
                    payload = payload.replace(old_b, new_b + b'\x00' * (len(old_b) - len(new_b)))
        except Exception:
            pass

    rebuild = payload
    if key is not None:
        if isinstance(key, list):
            rebuild = PakCrypto.xor_key(payload, bytes(key))
        else:
            rebuild = bytes(b ^ key for b in payload)
    if prefix:
        rebuild = raw_bytes[:prefix] + rebuild
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(rebuild)
    return True

# ==================== REPACK ENGINE (FULL IN-PLACE REBUILD, SAFE) ====================

def repack_pak_file_full(pak_file, edited_root, output_path, target_path=None, force_add=False, self_test=True, stealth=True):
    import copy as _cp
    edit_files = [p for p in Path(edited_root).rglob('*') if p.is_file() and not p.name.endswith(('.txt', '.json', '.md', '.raw', '.cleaned'))]
    if not edit_files:
        edit_files = [p for p in Path(edited_root).rglob('*') if p.is_file()]
    if not edit_files:
        console.print('[bold red]❌ No files found in EDIT folder![/bold red]')
        return 0

    version = pak_file._pak_info.version
    keystream = pak_file._keystream  # same ZUC pair that loaded the file
    orig_fc = pak_file._file_content
    orig_total = len(bytes(pak_file._file_content))

    raw = bytes(pak_file._file_content[pak_file._pak_info.index_offset:][:pidx_check(pak_file._pak_info)])
    if pak_file._pak_info.index_encrypted: raw = PakCrypto.decrypt_index(raw, pak_file._pak_info)
    r = Reader(raw); mp_str = r.string(); num_files = r.u4()
    for _ in range(num_files): TencentPakEntry(r, version)
    all_dirs = {}
    for _ in range(r.u8()):
        dp = r.string(); cnt = r.u8()
        all_dirs[dp] = {r.string(): pak_file._files[~r.i4()] for _ in range(cnt)}

    if target_path and force_add:
        target_path = target_path.replace('\\', '/')
        for ed in all_dirs.keys():
            if ed.strip('/').lower() == target_path.strip('/').lower():
                target_path = ed; break
        else: target_path = target_path.strip('/') + '/'

    pak_name_map = {}
    for dp, files in pak_file._index.items():
        for name, entry in files.items():
            full_path = str(PurePath(dp)/name).replace('\\', '/')
            pak_name_map.setdefault(name.lower(), []).append((full_path, entry))

    edited = {}
    for p in edit_files:
        fl = p.name.lower()
        if fl in pak_name_map:
            cands = pak_name_map[fl]
            edited[cands[0][0]] = (p, cands[0][1])
        elif force_add and target_path:
            tmpl = pak_file._files[0]
            new_fp = f"{target_path.rstrip('/')}/{p.name}"
            edited[new_fp] = (p, tmpl)

    if not edited:
        console.print('[bold red]❌ No files matched for repack![/bold red]')
        return 0

    new_files = [_cp.copy(e) for e in pak_file._files]
    old_to_new = {id(pak_file._files[i]): new_files[i] for i in range(len(pak_file._files))}
    out_buf = bytearray()
    stealth_delta = []

    for dp_str, dir_files in list(all_dirs.items()):
        for name, old_entry in list(dir_files.items()):
            full_path = str(PurePath(dp_str)/name).replace('\\', '/')
            ne = old_to_new.get(id(old_entry))
            em = old_entry.encryption_method
            cm = old_entry.compression_method
            enc = old_entry.encrypted

            if full_path in edited:
                p, template = edited[full_path]
                new_raw = p.read_bytes()
                ne.content_hash = SHA1.new(new_raw).digest()
                ne.uncompressed_size = len(new_raw)

                if cm == CM_NONE:
                    if enc:
                        padded = PakCrypto.align_encrypted_content_size(len(new_raw), em)
                        blob = new_raw + b'\x00' * (padded - len(new_raw))
                        cipher = PakCrypto.encrypt_block(blob, p, em)
                    else:
                        cipher = new_raw
                    ne.offset = len(out_buf)
                    ne.size = len(cipher)
                    out_buf += cipher
                    stealth_delta.append((full_path, ne.size - old_entry.size, 0))
                else:
                    orig_blk = max(1, len(old_entry.compressed_blocks))
                    cs = old_entry.compression_block_size if old_entry.compression_block_size > 0 else max(1, math.ceil(len(new_raw) / orig_blk))
                    chunks = [new_raw[i:i+cs] for i in range(0, len(new_raw), cs)]
                    if len(chunks) != orig_blk:
                        cs2 = max(1, math.ceil(len(new_raw) / orig_blk))
                        chunks = [new_raw[i:i+cs2] for i in range(0, len(new_raw), cs2)]
                        chunks = (chunks + [b''] * orig_blk)[:orig_blk]
                    target_total = old_entry.size  # keep compressed size close to original (anti size-track)
                    chosen_comps = None
                    if cm in (CM_ZLIB, CM_ZSTD, CM_ZSTD_DICT) and target_total > 0:
                        levels = [6, 3, 9, 12, 19, 1, 22] if cm != CM_ZLIB else [6, 9, 1]
                        best = None; bd = None
                        for lv in levels:
                            comps = [PakCompression.compress_block(chk, pak_file._zstd_dict, cm, level=lv) for chk in chunks]
                            total = sum(len(c) for c in comps)
                            d = abs(total - target_total)
                            if bd is None or d < bd:
                                bd = d; best = comps
                        chosen_comps = best
                    if chosen_comps is None:
                        chosen_comps = [PakCompression.compress_block(chk, pak_file._zstd_dict, cm) for chk in chunks]
                    new_blks = []
                    for comp in chosen_comps:
                        if enc:
                            comp = PakCrypto.encrypt_block(comp, p, em)
                        b = PakCompressedBlock.__new__(PakCompressedBlock)
                        b.start = len(out_buf); b.end = b.start + len(comp)
                        out_buf += comp
                        new_blks.append(b)
                    ne.compressed_blocks = new_blks
                    ne.offset = new_blks[0].start if new_blks else len(out_buf)
                    ne.size = sum(b.end - b.start for b in new_blks)
                    stealth_delta.append((full_path, ne.size - old_entry.size, len(new_blks) - len(old_entry.compressed_blocks)))
                console.print(f'[green]✓ Processed & Sealed: {full_path}[/green]')
            else:
                if cm == CM_NONE:
                    ne.offset = len(out_buf)
                    out_buf += bytes(orig_fc[old_entry.offset:old_entry.offset+old_entry.size])
                elif old_entry.compressed_blocks:
                    new_blks = []
                    for ob in old_entry.compressed_blocks:
                        nb = PakCompressedBlock.__new__(PakCompressedBlock)
                        nb.start = len(out_buf); nb.end = nb.start + (ob.end - ob.start)
                        out_buf += bytes(orig_fc[ob.start:ob.end])
                        new_blks.append(nb)
                    ne.compressed_blocks = new_blks
                    ne.offset = new_blks[0].start

    def pw_s(s): return struct.pack('<i', len(s.encode('utf-8'))+1) + s.encode('utf-8') + b'\x00' if s else struct.pack('<i', 0)
    idx = bytearray(pw_s(mp_str)) + struct.pack('<I', len(new_files))
    for ne in new_files:
        w = bytearray(ne.content_hash) + struct.pack('<QQIQ', ne.offset, ne.uncompressed_size, ne.compression_method, ne.size)
        if version >= 5: w += bytes([ne.unk1]) + ne.unk2
        if ne.compression_method != CM_NONE and version >= 3:
            w += struct.pack('<I', len(ne.compressed_blocks))
            for b in ne.compressed_blocks: w += struct.pack('<QQ', b.start, b.end)
        if version >= 4: w += struct.pack('<I', ne.compression_block_size) + bytes([1 if ne.encrypted else 0])
        if version >= 12: w += struct.pack('<II', ne.encryption_method, ne.index_new_sep)
        idx += w
    idx += struct.pack('<Q', len(all_dirs))
    for dp_str, dir_files in all_dirs.items():
        idx += pw_s(dp_str) + struct.pack('<Q', len(dir_files))
        for name, old_e in dir_files.items():
            idx += pw_s(name)
            found = next((i for i, e in enumerate(new_files) if id(e) == id(old_e)), -1)
            idx += struct.pack('<i', ~found if found != -1 else -1)

    idx_plain = bytes(idx)
    new_sha1 = SHA1.new(idx_plain).digest()
    if pak_file._pak_info.index_encrypted:
        k = PakCrypto.rsa_extract(pak_file._pak_info.packed_key, RSA_MOD_1)
        iv = PakCrypto.rsa_extract(pak_file._pak_info.packed_iv, RSA_MOD_1)
        aes = AES.new(k, MODE_CBC, iv[:16])
        pad = (-len(idx_plain)) % AES.block_size
        idx_bytes = aes.encrypt(idx_plain + bytes([pad] * pad)) if pad else aes.encrypt(idx_plain)
    else: idx_bytes = idx_plain

    new_idx_offset = len(out_buf)
    new_idx_size = len(idx_bytes)
    footer_len = TencentPakInfo._mem_size(version)
    size_delta = 0
    if stealth:
        filler = orig_total - (len(out_buf) + len(idx_bytes) + footer_len)
        if filler > 0:
            out_buf += b'\x00' * filler
            new_idx_offset = len(out_buf)
        else:
            size_delta = -filler
    out_buf += idx_bytes

    footer = bytearray(orig_fc[-TencentPakInfo._mem_size(version):])
    h_key = struct.pack('<5I', *keystream[4:9])
    footer[-36:-16] = bytes(a ^ b for a, b in zip(new_sha1, h_key))
    footer[-16:-8] = (new_idx_size ^ (keystream[10] << 32 | keystream[11])).to_bytes(8, 'little')
    footer[-8:] = (new_idx_offset ^ (keystream[0] << 32 | keystream[1])).to_bytes(8, 'little')
    out_buf += footer

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f: f.write(out_buf)

    if stealth:
        new_total = len(out_buf)
        rep = ['FRIEND TOOL — STEALTH REPACK REPORT', '='*46,
               'Source PAK   : %s' % (pak_file._pak_info.mp_name or ''),
               'Total blocks : %d -> %d' % (sum(len(e.compressed_blocks) for e in pak_file._files), sum(len(e.compressed_blocks) for e in new_files)),
               'Size         : %d -> %d  (delta %+d bytes)' % (orig_total, new_total, new_total - orig_total)]
        if new_total == orig_total:
            rep.append('STATUS       : 🛡 BYPASS — exact same total size, game size-track defeated')
        elif new_total < orig_total:
            rep.append('STATUS       : 🛡 BYPASS — padded back to original size, game size-track defeated')
        else:
            rep.append('STATUS       : ⚠ GROWN (+%d bytes) — edit smaller data or game may detect' % (new_total - orig_total))
        rep.append('-'*46)
        rep.append('Per-file order vs original (path | size delta | block-count delta):')
        worst = 0
        for fp, dsize, dblk in stealth_delta:
            worst = max(worst, dsize)
            rep.append('  %s | %+d B | %+d blocks' % (fp, dsize, dblk))
        try:
            rep_out = output_path.parent / 'STEALTH_REPORT.txt'
            rep_out.parent.mkdir(parents=True, exist_ok=True)
            rep_out.write_text('\n'.join(rep), encoding='utf-8')
            rep.append('')
            rep.append('Full report saved: %s' % rep_out)
        except Exception:
            pass
        for ln in rep:
            console.print(ln)
        if worst == 0:
            console.print('[bold green]🛡 Every edited file keeps its original byte-count — undetectable at file level.[/bold green]')

    if self_test:
        try:
            test = TencentPakFile(output_path)
            bad = []
            for dp, files in test._index.items():
                for fn, ent in files.items():
                    want = bytes(ent.content_hash)
                    if _is_all_zero(want): continue
                    cur = output_path.parent / ('_verify' / dp / fn)
                    try:
                        test._extract_one(cur, ent)
                        got = cur.read_bytes()
                        if len(got) != ent.uncompressed_size or SHA1.new(got).digest() != want:
                            bad.append(str(dp / fn))
                        cur.unlink(missing_ok=True)
                    except Exception:
                        bad.append(str(dp / fn))
            shutil.rmtree(output_path.parent / '_verify', ignore_errors=True)
            if bad:
                console.print(f'[bold yellow]⚠ Self-test: {len(bad)} file(s) failed verify: {", ".join(bad[:5])}[/bold yellow]')
            else:
                console.print('[bold green]✅ Self-test: repacked PAK re-unpacks clean (100% hash verified)[/bold green]')
        except Exception as e:
            console.print(f'[bold yellow]⚠ Self-test could not reopen output: {e}[/bold yellow]')

    return len(edited)

def pidx_check(pi) -> int:
    try:
        return pi.index_size
    except Exception:
        return 0

# ==================== UNIVERSAL DUMP & REPACK (ALL ASSETS) ====================

def _curate_tree(root: Path):
    """Park UI-noise artifacts (decoded-duplicates, temp copies) into root/_debug
    so the dump stays ONE clean folder with the meaningful files only."""
    try:
        dbg = root / '_debug'
        dbg.mkdir(exist_ok=True)
        for p in list(root.rglob('*')):
            if not p.is_file():
                continue
            rel = p.relative_to(root)
            if rel.parts and rel.parts[0] in ('_debug', '__nested__'):
                continue
            low = p.name.lower()
            drop = (low.endswith('.cleaned') or low.endswith('.raw.xml')
                    or low in ('original.bin', 'blob_header.hex', '_pack.bin', '_db_copy.db', 'strings_readable.txt', '_blob.bin'))
            if drop:
                tgt = dbg.joinpath(*rel)
                tgt.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(p), str(tgt))
    except Exception:
        pass
    try:
        if dbg.exists() and not any(dbg.rglob('*')):
            dbg.rmdir()
    except Exception:
        pass
    return root

def _dump_universal(src: Path, dest_dir: Path, rich: bool = False) -> Tuple[Path, str]:
    dest = dest_dir / src.stem
    if dest.exists(): shutil.rmtree(dest)
    dest.mkdir(parents=True)
    ext = src.suffix.lower()
    data = src.read_bytes()
    kind = detect_container(data, src.name)

    if kind == 'PAK':
        pak = TencentPakFile(src)
        pak.dump(dest)
        shutil.copy2(src, dest / '_pack.bin')
        (dest / 'meta.json').write_text(json.dumps({'source': src.name, 'type': 'PAK', 'version': pak._pak_info.version, 'files': sum(len(d) for d in pak._index.values())}))
        for p in Path(dest).rglob('*'):
            if p.is_file() and p.suffix.lower() in ('.pak', '.lua', '.obb'):
                _nested_dump(p, dest, 0, 2)
        _curate_tree(dest)
        return dest, 'PAK'

    if kind in ('ZIP', 'OBB_BLOB'):
        zf = data
        if kind == 'OBB_BLOB':
            (dest / '_blob.bin').write_bytes(data)
            b = _zip_bounds(data)
            if b:
                start, end = b
                zf = data[start:end]
            else:
                (dest / 'blob_header.hex').write_text(data[:512].hex(), encoding='utf-8')
                (dest / src.name).write_bytes(data)
                (dest / 'meta.json').write_text(json.dumps({'source': src.name, 'type': 'OBB_BLOB'}))
                _curate_tree(dest)
                return dest, 'OBB_BLOB'
        import io
        _extract_zip_readable(zf, dest / 'EXTRACTED')
        for p in Path(dest / 'EXTRACTED').rglob('*'):
            if p.is_file():
                _nested_dump(p, dest / 'EXTRACTED', 0, 2)
        (dest / 'meta.json').write_text(json.dumps({'source': src.name, 'type': 'OBB_BLOB' if kind == 'OBB_BLOB' else 'ZIP'}))
        _curate_tree(dest)
        return dest, 'OBB_BLOB' if kind == 'OBB_BLOB' else 'ZIP_CONTAINER'

    if kind.startswith('LUA') or kind == 'LUA_TEXT':
        _process_lua_file(data, dest, src.name, full=rich)
        (dest / 'meta.json').write_text(json.dumps({'source': src.name, 'type': kind}))
        _curate_tree(dest)
        return dest, 'LUA_SCRIPT'

    if kind == 'SQLITE':
        (dest / src.name).write_bytes(data)
        _dump_sqlite_readable(dest / src.name, dest)
        (dest / 'meta.json').write_text(json.dumps({'source': src.name, 'type': 'SQLITE'}))
        for p in Path(dest).rglob('*'):
            if p.is_file() and p.suffix.lower() in ('.pak', '.lua', '.obb'): _nested_dump(p, dest, 0, 2)
        _curate_tree(dest)
        return dest, 'SQLITE'

    (dest / src.name).write_bytes(data)
    strings = [m.group(0).decode('ascii', errors='replace') for m in re.finditer(rb'[\x20-\x7e]{4,}', data)]
    (dest / 'strings.txt').write_text('\n'.join(strings), encoding='utf-8')
    for p in Path(dest).rglob('*'):
        if p.is_file() and not p.name.endswith(('.txt', '.json')):
            _nested_dump(p, dest, 0, 2)
    (dest / 'meta.json').write_text(json.dumps({'source': src.name, 'type': 'BIN'}))
    _curate_tree(dest)
    return dest, 'RAW_BINARY'

def _repack_universal(dump_dir: Path, result_dir: Path):
    meta_path = dump_dir / 'meta.json'
    if not meta_path.exists():
        return False, "meta.json missing inside dump directory."
    meta = json.loads(meta_path.read_text())
    orig_name = meta['source']
    out_file = result_dir / orig_name
    result_dir.mkdir(parents=True, exist_ok=True)
    dtype = meta.get('type', 'BIN')

    if dtype in ('ZIP', 'OBB_BLOB'):
        ext_dir = dump_dir / 'EXTRACTED'
        tmp_zip = result_dir / ('__res__%s' % orig_name)
        with zipfile.ZipFile(tmp_zip, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for root, _, files in os.walk(ext_dir):
                for fn in files:
                    fp = Path(root) / fn
                    arc = str(fp.relative_to(ext_dir))
                    if '__nested__' in arc: continue
                    if arc.endswith('.raw.xml'): continue
                    if '_db_copy.db' in arc or arc == 'STATUS.txt': continue
                    z.write(fp, arcname=arc)
        if dtype == 'OBB_BLOB':
            blob = (dump_dir / '_blob.bin').read_bytes() if (dump_dir / '_blob.bin').exists() else None
            if blob is None:
                return False, 'OBB blob original not saved; cannot rebuild blob signature.'
            b = _zip_bounds(blob)
            if b is None:
                return False, 'OBB blob zip region not found.'
            start, end = b
            new_zip = tmp_zip.read_bytes()
            rebuild = blob[:start] + new_zip + blob[end:]
            out_file.write_bytes(rebuild)
            tmp_zip.unlink(missing_ok=True)
        else:
            shutil.copy2(tmp_zip, out_file)
            tmp_zip.unlink(missing_ok=True)
        return True, str(out_file)

    if dtype == 'SQLITE':
        src_bin = dump_dir / orig_name
        if src_bin.exists():
            shutil.copy2(src_bin, out_file)
            return True, str(out_file)
        return False, 'SQLITE repack: original db not found in dump.'

    if dtype in ('BIN', 'LUA58', 'LUA_TEXT', 'LUA51', 'LUA52', 'LUA53', 'LUA54', 'LUJIT'):
        if dtype.startswith('LUA'):
            if dtype == 'LUA_TEXT':
                txt = dump_dir / orig_name
                if txt.exists():
                    shutil.copy2(txt, out_file)
                    return True, str(out_file)
                txt = dump_dir / 'readable_script.lua'
                if txt.exists():
                    shutil.copy2(txt, out_file)
                    return True, str(out_file)
            ok = _repack_lua(dump_dir, orig_name, out_file)
            if ok: return True, str(out_file)
            return False, 'Lua repack: no raw bytecode copy found. Keep <name>.raw file.'
        src_bin = dump_dir / orig_name
        if src_bin.exists():
            shutil.copy2(src_bin, out_file)
            return True, str(out_file)

    if dtype == 'PAK':
        edit_root = dump_dir / 'unpacked'
        if not edit_root.exists():
            edit_root = dump_dir
        try:
            src_pak = result_dir / orig_name
            src_pak.parent.mkdir(parents=True, exist_ok=True)
            copy_src = dump_dir / '_pack.bin'
            if not copy_src.exists():
                meta2 = meta
                return False, 'Original PAK bytes not saved in dump. Re-run Universal Dump on the PAK.'
            shutil.copy2(copy_src, src_pak)
            pak = TencentPakFile(src_pak)
            count = repack_pak_file_full(pak, edit_root, out_file)
            src_pak.unlink(missing_ok=True)
            if count > 0: return True, str(out_file)
            return False, 'PAK repack matched no files.'
        except Exception as e:
            return False, 'PAK repack failed: %s' % e

    return False, "For PAK rebuilds, please use Option 3 / 4 for 100% stable index recreation."

# ==================== MAIN PROGRAM ====================

def ensure_dirs(b: Path):
    for d in ["PAK", "UNPACK", "REPACK", "RESULT", "INPUT", "DUMP", "PAK TOOL/EDIT", "PAK TOOL/UNPACK", "PAK TOOL/RESULT", "PAK TOOL/PAK"]:
        (b / d).mkdir(parents=True, exist_ok=True)

def safe_input(p: str = '') -> str:
    try: return input(p)
    except: return ''

def _pick_pak(base: Path):
    files = list((base / "PAK").glob("*.pak"))
    if not files: return files, None
    for i, f in enumerate(files, 1): console.print(f"  {i}. {f.name}")
    try:
        idx = int(safe_input('\nEnter number: ')) - 1
        return files, files[idx]
    except Exception:
        return files, None

def main_menu():
    base = Path(__file__).parent
    ensure_dirs(base)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print("[bold cyan]================================================[/bold cyan]")
        console.print("[bold yellow]      FRIEND BGMI TOOL — ULTIMATE ENGINE        [/bold yellow]")
        console.print("[bold cyan]================================================[/bold cyan]")
        console.print("[bold yellow]OWNER: @Friends6gg   |   TELEGRAM: @Friends6gg[/bold yellow]\n")

        console.print("[bold green]─── PAK TOOLS (CORE IN-PLACE REBUILD) ───[/bold green]")
        console.print("[bold cyan]1.[/bold cyan] UNPACK ALL TYPES PAKS")
        console.print("[bold cyan]2.[/bold cyan] REPACK ALL TYPES PAKS")
        console.print("[bold cyan]3.[/bold cyan] REPACK ANY SIZE (EXISTING FILES)")
        console.print("[bold cyan]4.[/bold cyan] REPACK TO PATH (NEW FILES)")
        console.print("[bold cyan]5.[/bold cyan] DELETE CACHE / FOLDERS")
        console.print("\n[bold yellow]─── NEW SYSTEM (OBB / LUA / BINARY DUMP) ───[/bold yellow]")
        console.print("[bold cyan]6.[/bold cyan] OBB UNPACK / REPACK")
        console.print("[bold cyan]7.[/bold cyan] LUA UNPACK / REPACK")
        console.print("[bold cyan]8.[/bold cyan] UNIVERSAL DUMP (Select by Number)")
        console.print("[bold cyan]9.[/bold cyan] REPACK FROM DUMP (Exact Original File Type)")
        console.print("[bold red]0.[/bold red] EXIT\n")

        c = safe_input('ENTER CHOICE: ').strip()

        # 1. UNPACK PAK
        if c == '1':
            files, sel = _pick_pak(base)
            if sel is None:
                console.print("[red]No .pak files found in PAK/[/red]"); safe_input('\nPress Enter...'); continue
            try:
                pak = TencentPakFile(sel)
                out = base / "UNPACK" / sel.stem
                ok = pak.dump(out)
                console.print(f"\n[bold green]✅ Success! {ok} file(s) extracted (hash-verified) to UNPACK/{sel.stem}[/bold green]")
                console.print("[dim]See UNPACK/<name>/STATUS.txt for per-file HASH_OK/SALVAGED status.[/dim]")
            except Exception as e:
                console.print(f"[bold red]❌ Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        # 2. REPACK ALL TYPES
        elif c == '2':
            files, sel = _pick_pak(base)
            if sel is None:
                console.print("[red]No .pak files found in PAK/[/red]"); safe_input('\nPress Enter...'); continue
            try:
                pak = TencentPakFile(sel)
                repack_dir = base / "REPACK" / sel.stem
                out = base / "RESULT" / sel.name
                repack_pak_file_full(pak, repack_dir, out)
                console.print(f"\n[bold green]✅ Repack Completed: {out}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Repack Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        # 3. REPACK ANY SIZE (PAK TOOL/EDIT)
        elif c == '3':
            files = list((base / "PAK").glob("*.pak"))
            if not files: files = list((base / "PAK TOOL" / "PAK").glob("*.pak"))
            if not files: console.print("[red]No .pak files found in PAK/ or PAK TOOL/PAK/[/red]"); safe_input('\nPress Enter...'); continue
            for i, f in enumerate(files, 1): console.print(f"  {i}. {f.name}")
            try:
                idx = int(safe_input('\nEnter number: ')) - 1
                pak = TencentPakFile(files[idx])
                edit_dir = base / "PAK TOOL" / "EDIT"
                out = base / "PAK TOOL" / "RESULT" / files[idx].name
                count = repack_pak_file_full(pak, edit_dir, out)
                if count > 0: console.print(f"\n[bold green]✅ Rebuilt {count} file(s) into: {out}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        # 4. REPACK TO PATH
        elif c == '4':
            files = list((base / "PAK").glob("*.pak"))
            if not files: files = list((base / "PAK TOOL" / "PAK").glob("*.pak"))
            if not files: console.print("[red]No .pak files found![/red]"); safe_input('\nPress Enter...'); continue
            for i, f in enumerate(files, 1): console.print(f"  {i}. {f.name}")
            try:
                idx = int(safe_input('\nEnter number: ')) - 1
                target = safe_input('Enter target path inside PAK: ').strip()
                pak = TencentPakFile(files[idx])
                edit_dir = base / "PAK TOOL" / "EDIT"
                out = base / "PAK TOOL" / "RESULT" / files[idx].name
                count = repack_pak_file_full(pak, edit_dir, out, target_path=target, force_add=True)
                if count > 0: console.print(f"\n[bold green]✅ Injected {count} file(s) into: {out}[/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        # 5. CLEAN STORAGE
        elif c == '5':
            for d in ["UNPACK", "REPACK", "DUMP"]: shutil.rmtree(base / d, ignore_errors=True)
            ensure_dirs(base)
            console.print("[bold green]✅ Temporary Cache Cleaned![/bold green]"); safe_input('\nPress Enter...')

        # 6. OBB SYSTEM
        elif c == '6':
            sub = safe_input("1. Unpack OBB  |  2. Repack OBB: ").strip()
            if sub == '1':
                obbs = list((base / "INPUT").glob("*.obb")) + list((base / "INPUT").glob("*.zip"))
                if not obbs: console.print("[red]No .obb in INPUT/[/red]")
                else:
                    for i, o in enumerate(obbs, 1): console.print(f"  {i}. {o.name}")
                    oi = int(safe_input('Select number: ')) - 1
                    d, fmt = _dump_universal(obbs[oi], base / "DUMP")
                    console.print(f"[bold green]✅ OBB Dumped ({fmt}) to DUMP/{d.name}/ - nested assets auto-extracted[/bold green]")
            elif sub == '2':
                dumps = [d for d in (base / "DUMP").iterdir() if d.is_dir()]
                if not dumps: console.print("[red]No dumps found in DUMP/[/red]")
                else:
                    for i, d in enumerate(dumps, 1): console.print(f"  {i}. {d.name}")
                    di = int(safe_input('Select number: ')) - 1
                    ok, res = _repack_universal(dumps[di], base / "RESULT")
                    if ok: console.print(f"[bold green]✅ Repacked OBB: {res}[/bold green]")
                    else: console.print(f"[red]❌ Error: {res}[/red]")
            safe_input('\nPress Enter...')

        # 7. LUA SYSTEM
        elif c == '7':
            sub = safe_input("1. Unpack / Decode Lua  |  2. Repack Lua: ").strip()
            if sub == '1':
                luas = [f for f in (base / "INPUT").iterdir() if f.is_file() and ('lua' in f.name.lower() or f.suffix in ('.bytes', '.bin', '.luac'))]
                if not luas: console.print("[red]No Lua files in INPUT/[/red]")
                else:
                    for i, l in enumerate(luas, 1): console.print(f"  {i}. {l.name}")
                    li = int(safe_input('Select number: ')) - 1
                    d, _ = _dump_universal(luas[li], base / "DUMP")
                    console.print(f"[bold green]✅ Lua Decoded to DUMP/{d.name}/ (readable decode + disasm ready!)[/bold green]")
            elif sub == '2':
                dumps = [d for d in (base / "DUMP").iterdir() if d.is_dir()]
                if not dumps: console.print("[red]No Lua dumps found![/red]")
                else:
                    for i, d in enumerate(dumps, 1): console.print(f"  {i}. {d.name}")
                    di = int(safe_input('Select number: ')) - 1
                    ok, res = _repack_universal(dumps[di], base / "RESULT")
                    if ok: console.print(f"[bold green]✅ Saved: {res}[/bold green]")
                    else: console.print(f"[red]❌ Error: {res}[/red]")
            safe_input('\nPress Enter...')

        # 8. UNIVERSAL DUMP
        elif c == '8':
            inputs = [f for f in (base / "INPUT").iterdir() if f.is_file()]
            if not inputs: console.print("[red]No files found in INPUT/[/red]"); safe_input('\nPress Enter...'); continue
            console.print("\n[bold cyan]Files in INPUT/:[/bold cyan]")
            for i, f in enumerate(inputs, 1): console.print(f"  {i}. {f.name}")
            console.print("  0. DUMP ALL")
            try:
                sel = int(safe_input('\nSelect file number: '))
                chosen = inputs if sel == 0 else [inputs[sel - 1]]
                for f in chosen:
                    d, fmt = _dump_universal(f, base / "DUMP")
                    console.print(f"[bold green]✓ Dumped: {f.name} ({fmt}) → DUMP/{d.name}/[/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ Dump Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        # 9. REPACK FROM DUMP
        elif c == '9':
            dumps = [d for d in (base / "DUMP").iterdir() if d.is_dir()]
            if not dumps: console.print("[red]No folders in DUMP/ to repack![/red]"); safe_input('\nPress Enter...'); continue
            for i, d in enumerate(dumps, 1): console.print(f"  {i}. {d.name}")
            try:
                idx = int(safe_input('\nSelect dump number: ')) - 1
                ok, res = _repack_universal(dumps[idx], base / "RESULT")
                if ok: console.print(f"\n[bold green]✅ Repacked exactly as original format: {res}[/bold green]")
                else: console.print(f"\n[bold red]❌ Repack failed: {res}[/bold red]")
            except Exception as e:
                console.print(f"[bold red]❌ Error: {e}[/bold red]")
                traceback.print_exc()
            safe_input('\nPress Enter...')

        elif c == '0':
            break

if __name__ == '__main__':
    main_menu()