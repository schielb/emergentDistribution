#include <iostream>
#include <stdlib.h>
#include <cmath>
using namespace std;

enum Sensor_t{Blue, Red, Green, Yellow, Purple, Orange, Pink, Brown, Black};

#define WIDTH 4
#define HEIGHT 4
#define NUM_ITERATIONS 5
#define NUM_VARS 8


float calculateSD(float data[], int num_vars) {
  float sum = 0.0, mean, standardDeviation = 0.0;
  int i;

  for(i = 0; i < num_vars; ++i) {
    sum += data[i];
  }

  mean = sum / num_vars;

  for(i = 0; i < num_vars; ++i) {
    standardDeviation += pow(data[i] - mean, 2);
  }

  return sqrt(standardDeviation / num_vars);
}

float calculatePC(Sensor_t * f_prev, int num_vars, int width, int height) {
    int length = width * height;
    float total_collisions = 0, potential_neighbors = 0;

    for (int i = 0; i < length; i++) {
        // Look up
        if (i / width != 0) {
            potential_neighbors++;
            if (f_prev[i] == f_prev[i - width]) total_collisions++;
        }

        // Look down
        if (i / width != height - 1) {
            potential_neighbors++;
            if (f_prev[i] == f_prev[i + width]) total_collisions++;
        }

        // Look right
        if (i % width != width - 1) {
            potential_neighbors++;
            if (f_prev[i] == f_prev[i + 1]) total_collisions++;
        }

        // Look left
        if (i % width != 0) {
            potential_neighbors++;
            if (f_prev[i] == f_prev[i - 1]) total_collisions++;
        }
    }
    return total_collisions / potential_neighbors;
}

void perform_analysis (Sensor_t * f_prev, int num_vars = NUM_VARS, int width = WIDTH, int height = HEIGHT) {
    int length = width * height;
    float * totals = new float[num_vars];

    for (int i = 0; i < length; i++) {
        totals[(int) f_prev[i]] += 1.0;
    }

    float stan_dev = calculateSD(totals, num_vars);
    float perc_col = calculatePC(f_prev, num_vars, width, height);

    printf("[%.4f, %.4f], ", stan_dev, perc_col);
}






void set_random(Sensor_t * f_next, int num_vars = NUM_VARS, int width = WIDTH, int height = HEIGHT) {
    int length = width * height;
    
    for (int i = 0; i < length; i++) {
        f_next[i] = Sensor_t(rand() % num_vars);
    }
}





int main() {
    Sensor_t field_1[WIDTH * HEIGHT];//, *field_2;

    // field_1 = new Sensor_t[WIDTH * HEIGHT];
    // field_2 = new Sensor_t[WIDTH * HEIGHT];
    //field_1


    

    srand(0xBEEFCAFE);
    
    //////////////// Completely random
    {
        cout << "Rand_rand = [";


        // Set the field first off
        //set_random(field_1);

        for (int i = 0; i < NUM_ITERATIONS; i++) {
            set_random(field_1);
            perform_analysis(field_1);
        }



        cout << "]\r\n\n";
    }



    // delete[] field_1;
    // delete[] field_2;

    return 0;
}