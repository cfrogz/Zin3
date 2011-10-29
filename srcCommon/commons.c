/*
 * commons.c
 *
 *  Created on: 25.10.2011
 *      Author: i0nsane
 */


#include <python2.6/Python.h>
#include <stdio.h>

ParseError = PyErr_NewException("parse.error", NULL, NULL);

static PyObject * commons_output( PyObject *self, PyObject *args){
	char *out0, *out1;

	if (!PyArg_ParseTuple(args, "ss", &out0, &out1)){
		//PyErr_SetString(ParseError, "Error while parsing arguments");
		return NULL;
	}

	printf("%s %s", out0, out1);
	return 0;
}

static PyMethodDef CommonsMethods[] = {
		{
				"commons_output", commons_output, METH_VARARGS,
				"Display two Strings printed by printf()."
		},
		{
				NULL, NULL, 0, NULL
		}
};

PyMODINIT_FUNC
initcommons(void){
	(void) Py_InitModule("commons", CommonsMethods);
}
