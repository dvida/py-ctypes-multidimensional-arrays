#include "myfunc.h"
#include <stdio.h>

double myfunc(double *arr, struct mystruct_t *data) {

	double result = 0.;

	// Go through all X data
	for(int i = 0; i < data->n; i++) {

		// Do something with the data

		result += data->x[i];

		data->x[i] += 1.0;

		data->sum += data->x[i];

		printf("arr[%d]: %f\n", i, arr[i]);
	}

	// Do something with 2D and 3D arrays
	data->y[0][0] = 1.0;
	data->z[0][0][0] = 99;

	return result;
}
