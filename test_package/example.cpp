// Test for easy_profiler Conan package
// Dmitriy Vetutnev, Odant, 2018


#include <easy/profiler.h>


#include <cstdlib>
#include <iostream>
#include <chrono>
#include <thread>


const std::size_t OBJECTS = 1000;


void modellingWorker(const char* threadName) {

    EASY_THREAD(threadName);


    volatile double *pos[OBJECTS];
    for (int i = 0; i < OBJECTS; ++i) {
        pos[i] = new volatile double[3];
    }

    {
        EASY_BLOCK("Collisions", profiler::ON, profiler::colors::Red);
        
        volatile int i, j;
        volatile double dist;
        
        for (i = 0; i < OBJECTS; ++i) {
            for (j = i + 1; j < OBJECTS; ++j) {
                
                EASY_BLOCK("Check");
                
                volatile double v[3];
                
                v[0] = pos[i][0] - pos[j][0];
                v[1] = pos[i][1] - pos[j][1];
                v[2] = pos[i][2] - pos[j][2];
                
                dist = v[0] * v[0] + v[1] * v[1] + v[2] * v[2];
                
                if (dist < 10000) {
                    dist *= dist;
                }
            }
        }
    }

    for (int i = 0; i < OBJECTS; ++i) {
        delete [] pos[i];
    }
}


int main(int, char**) {
    
    std::cout << "Objects count: " << OBJECTS << std::endl;

    auto start = std::chrono::system_clock::now();

    EASY_PROFILER_ENABLE;
    EASY_MAIN_THREAD;

    
    std::thread thread_first{modellingWorker, "Modelling thread first"};
    std::thread thread_second{modellingWorker, "Modelling thread second"};
    
    thread_first.join();
    thread_second.join();
    
    
    auto end = std::chrono::system_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Elapsed time: " << elapsed.count() << " usec" << std::endl;

    auto blocks_count = profiler::dumpBlocksToFile("example.prof");

    std::cout << "Blocks count: " << blocks_count << std::endl;
    
    return EXIT_SUCCESS;
}
