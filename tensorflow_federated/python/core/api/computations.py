# Copyright 2018, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Defines functions and classes for constructing TFF computations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow_federated.python.core.impl import computation_wrapper_instances


def tf_computation(*args):
  """Decorates or wraps Python functions and TF defuns as TFF computations.

  This symbol can be used as either a decorator (`@tf_computation`) or a wrapper
  applied to a function given to it as an argument. The supported patterns and
  examples of usage are as follows:

  1. Convert an existing function inline into a TFF computation. This is the
     simplest mode of usage, and how one can embed existing non-TFF code for
     use with the TFF framework. In this mode, one invokes `tf_computation()`
     with a pair of arguments, the first being a function/defun that contains
     the logic, and the second being the TFF type of the parameter:

     ```
     foo = tf_computation(lambda x: x > 10, tf.int32)
     ```

     After executing the above code snippet, `foo` becomes an instance of the
     abstract base class `Computation` (defined in computation_base). Like all
     computations, it has the `type_signature` property:

     ```
     str(foo.type_signature) == '(int32 -> bool)'
     ```

     The function passed as a parameter doesn't have to be a lambda, it can
     also be an existing Python function or a defun. Here's how to construct
     a computation from the standard TensorFlow operator `tf.add`:

     ```
     foo = tf_computation(tf.add, (tf.int32, tf.int32))
     ```

     The resulting type signature is as expected:
     ```
     str(foo.type_signature) == '(<int32,int32> -> int32)'
     ```

     If one intends to create a computation that doesn't accept any arguments,
     the type argument is simply omitted. The function must be a no-argument
     function as well:

     ```
     foo = tf_computation(lambda: tf.constant(10))
     ```

  2. Decorate a Python function or a TensorFlow defun with a TFF type to wrap
     it as a TFF computation. The only difference between this mode of usage
     and the one mentioned above is that instead of passing the function/defun
     as an argument, `@tf_computation` along with the optional type specifier
     is written above the function/defun's body.

     Here's an example of a computation that accepts a parameter:

     ```
     @tf_computation(tf.int32)
     def foo(x):
       return x > 10
     ```

     One can think of this mode of usage as merely a syntactic sugar for the
     example already given earlier:

     ```
     foo = tf_computation(lambda x: x > 10, tf.int32)
     ```

     Here's an example of a no-parameter computation:

     ```
     @tf_computation
     def foo():
       return tf.constant(10)
     ```

     Again, this is merely a syntactic sugar for the example given earlier:

     ```
     foo = tf_computation(lambda: tf.constant(10))
     ```

     If the Python function has multiple decorators, `@tf_computation` should
     be the outermost one (the one that appears first in the sequence).

  3. Create a polymorphic callable to be instantiated based on arguments,
     similarly to TensorFlow defuns that have been defined without an input
     signature.

     This mode of usage is symmetric to those above. One simply omits the type
     specifier, and applies `tf_computation` as a decorator or wrapper to a
     function/defun that does expect parameters.

     Here's an example of wrapping a lambda as a polymorphic callable:

     ```
     foo = tf_computation(lambda x, y: x > y)
     ```

     The resulting `foo` can be used in the same ways as if it were had the
     type been declared; the corresponding computation is simply created on
     demand, in the same way as how polymorphic TensorFlow defuns create and
     cache concrete function definitions for each combination of argument
     types.

     ```
     ...foo(1, 2)...
     ...foo(0.5, 0.3)...
     ```

     Here's an example of creating a polymorphic callable via decorator:

     ```
     @tf_computation
     def foo(x, y):
       return x > y
     ```

     The syntax is symmetric to all examples already shown.

  Args:
    *args: Either a function/defun, or TFF type spec, or both (function first),
      or neither, as documented in the 3 patterns and examples of usage above.

  Returns:
    If invoked with a function as an argument, returns a an instance of a TFF
    computation constructed based on this function. If called without one, as
    in the typical decorator style of usage, returns a callable that expects
    to be called with the function definition supplied as a parameter; see the
    patterns and examples of usage above.
  """
  return computation_wrapper_instances.tensorflow_wrapper(*args)
