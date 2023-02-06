/* -*- C++ -*- ------------------------------------------------------------
 
Copyright (c) 2007 Jesse Anders and Demian Nave http://cmldev.net/

The Configurable Math Library (CML) is distributed under the terms of the
Boost Software License, v1.0 (see cml/LICENSE for details).

 *-----------------------------------------------------------------------*/
/** @file
 *  @brief
 *
 *  The configurable matrix<> class.
 */

#ifndef cml_matrix_h
#define cml_matrix_h

#include "cml_core_common.h"

namespace cml {

/** A configurable matrix.
 *
 * This class encapsulates the notion of a matrix.  The ArrayType template
 * argument can be used to select the type of array to be used as internal
 * storage for a 2D array of type Element.
 *
 * @internal Unlike the previous version, this uses specializations to better
 * enable varied array and matrix types. For example, with the rebind method,
 * it's difficult to support external<> matrix types that should not be
 * assigned to.
 *
 * @internal All assignments to the matrix should go through UnrollAssignment,
 * which ensures that the source expression and the destination matrix have
 * the same size.  This is particularly important for dynamically-sized
 * matrices.
 */
template<typename Element, class ArrayType,
    typename BasisOrient = CML_DEFAULT_BASIS_ORIENTATION,
    typename Layout = CML_DEFAULT_ARRAY_LAYOUT> class matrix;

} // namespace cml

#include "cml_matrix_matrix_ops.h"
#include "cml_matrix_matrix_transpose.h"
#include "cml_matrix_matrix_rowcol.h"
#include "cml_matrix_matrix_mul.h"
#include "cml_matvec_matvec_mul.h"
#include "cml_matrix_matrix_functions.h"
#include "cml_matrix_lu.h"
#include "cml_matrix_inverse.h"
#include "cml_matrix_determinant.h"
#include "cml_matrix_matrix_print.h"

#include "cml_matrix_fixed.h"
#include "cml_matrix_dynamic.h"
#include "cml_matrix_external.h"

#endif

// -------------------------------------------------------------------------
// vim:ft=cpp
