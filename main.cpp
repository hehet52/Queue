#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <deque>
#include <thread>
#include <chrono>

using namespace std;


void render(const deque<string>& q, string op, string val) {
    system("cls"); 
    cout << "================================" << endl;
    cout << " cafemusolt." << op << "(\"" << val << "\")" << endl;
    cout << "--------------------------------" << endl;
    cout << "          CAFE MUSOLT           " << endl;
    cout << "--------------------------------" << endl;

    if (q.empty()) {
        cout << "        ( Empty Queue )         " << endl;
    }
    else {
        for (const auto& item : q) {
            cout << "  - " << item << endl;
        }
    }
    cout << "================================" << endl;


    this_thread::sleep_for(chrono::milliseconds(1500));
}

int main() {
    system("chcp 65001"); 

    deque<string> cafeQueue;
    const int MAX_SIZE = 10;

    ifstream file("menu.csv");
    if (!file.is_open()) {
        cout << "Error: menu.csv not found." << endl;
        return 1;
    }

    string line, name, id, w1, w2, w3;
    vector<string> all_words;
    getline(file, line); 

    while (getline(file, line)) {
        stringstream ss(line);
        getline(ss, name, ',');
        getline(ss, id, ',');
        getline(ss, w1, ',');
        getline(ss, w2, ',');
        getline(ss, w3, ',');
        all_words.push_back(w1);
        all_words.push_back(w2);
        all_words.push_back(w3);
    }
    file.close();

    //isEmpty
    render(cafeQueue, "isEmpty", "Check");

    //enqueue
    for (const auto& menu : all_words) {
        // 큐 크기 10 
        if (cafeQueue.size() >= MAX_SIZE) {
            string removed = cafeQueue.front();
            cafeQueue.pop_front(); //dequeue
            render(cafeQueue, "dequeue", removed);
        }

        cafeQueue.push_back(menu); //enqueue
        render(cafeQueue, "enqueue", menu);

        //front
        if (cafeQueue.size() == 5) {
            render(cafeQueue, "front", cafeQueue.front());
        }
    }

    //dequeue, clear
    if (!cafeQueue.empty()) {
        string val = cafeQueue.front();
        cafeQueue.pop_front();
        render(cafeQueue, "dequeue", val);
    }

    cafeQueue.clear(); //clear
    render(cafeQueue, "clear", "All");

    render(cafeQueue, "isEmpty", "Final Check");

    return 0;
}