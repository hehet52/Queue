#include <iostream>
#include <deque>
#include <string>
#include <thread>
#include <chrono>
using namespace std;

// Queue 클래스
template <typename T>
class Queue {
private:
    deque<T> data;

public:
    void enqueue(const T& x) {
        data.push_back(x);
    }

    T dequeue() {
        T front = data.front();
        data.pop_front();
        return front;
    }

    T front() const {
        return data.front();
    }

    bool isEmpty() const {
        return data.empty();
    }

    void clear() {
        data.clear();
    }

    int size() const {
        return data.size();
    }

    deque<T> getData() const {
        return data;
    }
};

void draw(Queue<string> q, string action) {
    system("cls");

    cout << "카페무솔트." << action << "\n\n";

    cout << "                    ┌───────────────┐\n";
    cout << "                    │   카페무솔트   │\n";
    cout << "                    ├───────────────┤\n";

    deque<string> temp = q.getData();
    int n = temp.size();

    for (int i = n - 1; i >= 0; i--) {
        cout << "                    │ " << temp[i];

        int space = 15 - temp[i].length();
        for (int j = 0; j < space; j++) cout << " ";

        cout << "│\n";


        if (i != 0) {
            cout << "                    ├───────────────┤\n";
        }
    }

    cout << "                    └───────────────┘\n";
}

int main() {
    Queue<string> q;

    string menu[] = {
        "카페라떼","청포도에이드","레몬에이드","말차라떼",
        "초코스콘","플레인휘낭시에","초코휘낭시에",
        "피넛라떼","매실티","레몬티",
        "초코라떼","카페모카","피넛라떼","산과아메리카노"
    };

    int size = sizeof(menu) / sizeof(menu[0]);

    for (int i = 0; i < size; i++) {

        if (q.size() == 10) {
            string removed = q.dequeue();
            draw(q, "dequeue() → " + removed);
            this_thread::sleep_for(chrono::milliseconds(700));
        }

        q.enqueue(menu[i]);
        draw(q, "enqueue(\"" + menu[i] + "\")");
        this_thread::sleep_for(chrono::milliseconds(700));
    }


    if (!q.isEmpty()) {
        string removed = q.dequeue();
        draw(q, "dequeue() → " + removed);
        this_thread::sleep_for(chrono::milliseconds(1000));
    }


    if (q.isEmpty()) {}

    this_thread::sleep_for(chrono::milliseconds(500));


    q.clear();
    draw(q, "clear()");
    this_thread::sleep_for(chrono::milliseconds(1000));

    if (q.isEmpty()) {}

    return 0;
}