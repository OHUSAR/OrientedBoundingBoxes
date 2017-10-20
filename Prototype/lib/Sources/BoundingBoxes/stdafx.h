// stdafx.h : include file for standard system include files,
// or project specific include files that are used frequently, but
// are changed infrequently
//

#pragma once

#include <Windows.h>

#define WIN32_LEAN_AND_MEAN             // Exclude rarely-used stuff from Windows headers

#include "../Utils/GlobalTypes.h"
#include "../Utils/UtilsLib.h"

#include "../NumericOptimization/MathLib.h"

using namespace NumericOptimization;
using namespace NumericOptimization::Utils;
using namespace NumericOptimization::Utils::Copy;
using namespace NumericOptimization::Utils::Exceptions;

using namespace NumericOptimization::Math::LinearAlgebra;