// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//

#pragma once

#include <Windows.h>

#define WIN32_LEAN_AND_MEAN             // Exclude rarely-used stuff from Windows headers

#include "Macros.h"

#include "GlobalTypes.h"
#include "Copy.h"
#include "MemoryAllocator.h"
#include "Exception.h"

using namespace NumericOptimization;
using namespace NumericOptimization::Utils;
using namespace NumericOptimization::Utils::Copy;
using namespace NumericOptimization::Utils::Exceptions;
