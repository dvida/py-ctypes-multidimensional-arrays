
// Structure which containes the data
struct mystruct_t {

	// Number of elements
	int n;

	// Scalar result stored in this variable
	double sum;

	// 1D I/O array
	double *x;

	// 2D I/O array
	double **y;

	// 3D I/O array
	double ***z;
};

// Function prototype
double myfunc(double *arr, struct mystruct_t *data);
