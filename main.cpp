#include <iostream>
#include <stdlib.h>
#include <cmath>
#include <algorithm>
#include <ctime>
#include <sys/time.h>
#include <chrono>
using namespace std;
using namespace chrono;

enum Sensor_t{Blue, Red, Green, Yellow, Purple, Orange, Pink, Brown, Black};

#define WIDTH 256
#define HEIGHT 256
#define NUM_ITERATIONS 100
#define NUM_VARS 8

#define INIT_VAL 1.0
#define DEC_VAL 0.1
#define THRESH 0.5


float calculateSD(float * data, int num_vars) {
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

void calculateDC(float** centers, int num_vars, int width, int height) {
    float center_x = (float)width / 2.0;
    float center_y = (float)height / 2.0;

    cout << "[";

    for (int i = 0; i < num_vars; i++) {
        float dist_x = abs(center_x - centers[i][0]);
        float dist_y = abs(center_y - centers[i][1]);

        float a2 = pow(dist_x, 2);
        float b2 = pow(dist_y, 2);
        float c = sqrt(a2 + b2);

        printf("%.4f", c);

        if (i < num_vars - 1) cout << ", ";
    }

    cout << "]]";
}

void perform_analysis (Sensor_t * f_prev, const int num_vars = NUM_VARS, int width = WIDTH, int height = HEIGHT) {
    int length = width * height;
    float * totals = new float[num_vars];

    for (int i = 0; i < num_vars; i++) {
        totals[i] = 0.01;
    }

    float ** centers;
    centers = new float*[num_vars];

    for(int i = 0; i < num_vars; i++){
        centers[i] = new float[2];

        centers[i][0] = -0.01;
        centers[i][1] = -0.01;
    }

    for (int i = 0; i < length; i++) {
        totals[(int) f_prev[i]] += 1.0;

        // Get the x
        centers[(int) f_prev[i]][0] += (float)(i % width);
        // Get the y
        centers[(int) f_prev[i]][1] += (float)(i / width);

    }

    // Calculate the centers - average position of each var
    for (int i = 0; i < num_vars; i++) {
        if (totals[i] > 0.5) {
            float
                c0 = centers[i][0],
                c1 = centers[i][1],
                t = totals[i];
            centers[i][0] /= totals[i];
            centers[i][1] /= totals[i];
        }
    }

    float stan_dev = calculateSD(totals, num_vars);
    float perc_col = calculatePC(f_prev, num_vars, width, height);

    printf("[%.4f, %.4f, ", stan_dev, perc_col);

    calculateDC(centers, num_vars, width, height);

    for (int i = 0; i < num_vars; i++) {
        delete[] centers[i];
    }

    delete[] centers;
    
}






void set_random(Sensor_t * f_next, int num_vars = NUM_VARS, int width = WIDTH, int height = HEIGHT) {
    int length = width * height;
    
    for (int i = 0; i < length; i++) {
        f_next[i] = Sensor_t(rand() % num_vars);
    }
}

void cycle(Sensor_t * f_next, int num_vars = NUM_VARS, int width = WIDTH, int height = HEIGHT) {
    int length = width * height;

    for (int i = 0; i < length; i++) {
        int cur_val = (int) f_next[i];
        f_next[i] = Sensor_t((cur_val + 1) % num_vars);
    }
}

void emerge_step(Sensor_t * f_dst, Sensor_t * f_src, 
    const float init_prob, const float dec_amount, const float thresh,
    const int num_vars = NUM_VARS, int width = WIDTH, int height = HEIGHT) {
    int length = width * height;
    
    float probs[num_vars];

    

    for (int i = 0; i < length; i++) {
        for (int j = 0; j < num_vars; j++) {
            probs[j] = init_prob;
        }
        
        // Look up
        if (i / width != 0) {
            probs[(int)f_src[i - width]] -= dec_amount;
        }

        // Look down
        if (i / width != height - 1) {
            probs[(int)f_src[i + width]] -= dec_amount;
        }

        // Look right
        if (i % width != width - 1) {
            probs[(int)f_src[i + 1]] -= dec_amount;
        }

        // Look left
        if (i % width != 0) {
            probs[(int)f_src[i - 1]] -= dec_amount;
        }

        float 
            max = *max_element(probs, probs + num_vars),
            min = *min_element(probs, probs + num_vars);

        int num_pass = 0;

        // We have now taken all values into account, we need to normalize
        // If all values are equal, do this explicitly to avoid dividng by 0
        if (abs(max - min) < (dec_amount / 2)) {
            for (int j = 0; j < num_vars; j++) probs[j] = 1.0;

            num_pass = num_vars;
        }
        else {
            for (int j = 0; j < num_vars; j++) {
                probs[j] /= max;
                if (probs[j] > thresh) {
                    num_pass++;
                }
            }
        }

        int next_sure = rand() % num_vars;

        if (num_pass != 0) {
            int *poss_next = new int[num_pass];

            int idx = 0;
            for (int j = 0; j < num_vars; j++) {
                if (probs[j] > thresh) {
                    poss_next[idx] = j;
                    idx++;
                }
            }

            next_sure = poss_next[rand() % num_pass];
            delete[] poss_next;
        }

        f_dst[i] = Sensor_t(next_sure);
    }

    



    
}





int main() {
    Sensor_t field_1[WIDTH * HEIGHT], field_2[WIDTH * HEIGHT];

    // field_1 = new Sensor_t[WIDTH * HEIGHT];
    // field_2 = new Sensor_t[WIDTH * HEIGHT];
    //field_1


    

    srand(0xBEEFCAFE);

    auto start1 = high_resolution_clock::now();
    
    
    //////////////// Completely random
    {
        cout << "Rand_rand = [";


        // Set the field first off
        //set_random(field_1);

        for (int i = 0; i < NUM_ITERATIONS; i++) {
            set_random(field_1);
            perform_analysis(field_1);

            if (i < NUM_ITERATIONS - 1) {
                cout << ", ";
            }
        }

        cout << "]\r\n";
    }
    
    
    auto t2 = high_resolution_clock::now();

    auto duration = duration_cast<microseconds>(t2 - start1);
    
    cout << "time_rand = " << (double)(duration.count() / 1000.0) << "\r\n\n";

    //////////////// Random loop
    {
        cout << "Rand_loop = [";

        set_random(field_1);

        for (int i = 0; i < NUM_ITERATIONS; i++) {
            cycle(field_1);
            perform_analysis(field_1);

            if (i < NUM_ITERATIONS - 1) {
                cout << ", ";
            }
        }

        cout << "]\r\n";
    }
    
    
    auto t3 = high_resolution_clock::now();

    auto duration1 = duration_cast<microseconds>(t3 - t2);
    
    cout << "time_loop = " << (double)(duration1.count() / 1000.0) << "\r\n\n";


    //////////////// Emergent step
    {
        cout << "Emerge_step = [";

        set_random(field_1);

        Sensor_t 
            *f1 = field_1, 
            *f2 = field_2, 
            *tmp;

        for (int i = 0; i < NUM_ITERATIONS; i++) {
            emerge_step(f2, f1, INIT_VAL, DEC_VAL, THRESH);
            perform_analysis(f2);

            tmp = f1;
            f1 = f2;
            f2 = tmp;

            if (i < NUM_ITERATIONS - 1) {
                cout << ", ";
            }
        }

        cout << "]\r\n";
    }
    
    
    auto t4 = high_resolution_clock::now();

    auto duration2 = duration_cast<microseconds>(t4 - t3);
    
    cout << "time_emerge = " << (double)(duration2.count() / 1000.0) << "\r\n\n";

    // delete[] field_1;
    // delete[] field_2;

    return 0;
}