#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <queue> 
#include <vector>
#include <Windows.h>

using namespace std;

string trim(string s) {
    size_t first = s.find_first_not_of(" \t\r\n");
    if (string::npos == first) return "";
    size_t last = s.find_last_not_of(" \t\r\n");
    return s.substr(first, (last - first + 1));
}

void printQueue(queue<string> q, string currentName, string currentId) {
    vector<string> items;
    queue<string> tempQ = q;
    while (!tempQ.empty()) {
        items.push_back(tempQ.front());
        tempQ.pop();
    }

    cout << "\n[ User: " << currentName << " | ID: " << currentId << " ]" << endl;
    cout << "+---------------------------------+" << endl;
    cout << "|           CAFE MUSALT           |" << endl;
    cout << "+---------------------------------+" << endl;

    if (items.empty()) {
        cout << "|        ( Queue is Empty )       |" << endl;
    }
    else {
        for (int i = 0; i < (int)items.size(); i++) {
            if (i == 0)
                cout << "|  [FRONT] " << items[i] << " <--- Exit" << endl;
            else if (i == (int)items.size() - 1)
                cout << "|  [REAR ] " << items[i] << " <--- Entry" << endl;
            else
                cout << "|          " << items[i] << endl;
        }
    }
    cout << "+---------------------------------+" << endl;
    cout << "  Size: " << items.size() << " | Empty: " << (q.empty() ? "YES" : "NO") << endl;
}

void waitKey(string msg) {
    cout << "\n>> " << msg << " [Enter]";
    cin.clear();
    cin.ignore(100, '\n');
    system("cls");
}

int main() {
    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);

    ifstream file("카페무솔트.csv");
    if (!file.is_open()) { return 1; }

    string line;
    getline(file, line);

    struct Person { string name, id, w1, w2, w3; };
    vector<Person> people;

    while (getline(file, line)) {
        stringstream ss(line);
        Person p;
        getline(ss, p.name, ','); getline(ss, p.id, ',');
        getline(ss, p.w1, ','); getline(ss, p.w2, ','); getline(ss, p.w3, ',');
        p.name = trim(p.name); p.id = trim(p.id);
        p.w1 = trim(p.w1); p.w2 = trim(p.w2); p.w3 = trim(p.w3);
        people.push_back(p);
    }
    file.close();

    // === 여기서부터 추가된 선언부 ===
    queue<string> q;

    cout << "======================================" << endl;
    cout << ">> [SYSTEM] queue<string> q; Declared" << endl;
    cout << ">> [CHECK] Initial State isEmpty: " << (q.empty() ? "TRUE" : "FALSE") << endl;
    cout << "======================================" << endl;

    printQueue(q, "N/A", "N/A");
    waitKey("Queue initialized. Press Enter to start...");
    // === 여기까지 추가된 선언부 ===

    for (auto& p : people) {
        // 1. Enqueue 3개 진행
        vector<string> words = { p.w1, p.w2, p.w3 };
        for (auto& w : words) {
            q.push(w);
            cout << ">> [ENQUEUE] '" << w << "' added." << endl;
            printQueue(q, p.name, p.id);
            waitKey("Next step...");
        }

        // 2. Front 확인
        cout << ">> [FRONT] Current front item is: " << q.front() << endl;
        printQueue(q, p.name, p.id);
        waitKey("Peek finished. Now let's dequeue...");

        // 3. Dequeue 2개 진행 (1개만 남을 때까지)
        for (int i = 0; i < 2; i++) {
            cout << ">> [DEQUEUE] Removing: " << q.front() << endl;
            q.pop();
            printQueue(q, p.name, p.id);
            waitKey("One more dequeue...");
        }

        // 4. 마지막 1개 남았을 때 상태 확인 (isEmpty 테스트용)
        cout << ">> [CHECK] Is queue empty? " << (q.empty() ? "Yes" : "No") << endl;
        cout << ">> Only one item left. Let's CLEAR the queue now." << endl;
        printQueue(q, p.name, p.id);
        waitKey("Proceed to CLEAR...");

        // 5. Clear (나머지 1개 비우기)
        while (!q.empty()) {
            q.pop();
        }
        cout << ">> [CLEAR] Queue has been cleared." << endl;
        printQueue(q, p.name, p.id);
        waitKey("Next person's turn...");
    }

    return 0;
}