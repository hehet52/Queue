#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <queue> // stack에서 queue로 변경
#include <vector>
#include <Windows.h>
#include <conio.h>
#include <direct.h>

using namespace std;

string trim(string s) {
    s.erase(0, s.find_first_not_of(" \t\r\n"));
    if (s.find_last_not_of(" \t\r\n") != string::npos)
        s.erase(s.find_last_not_of(" \t\r\n") + 1);
    return s;
}

// 큐의 내용을 출력하는 함수
void printQueue(queue<string> q, string currentName, string currentId) {
    vector<string> items;
    // 큐는 앞에서부터 꺼내어 벡터에 담음
    while (!q.empty()) {
        items.push_back(q.front());
        q.pop();
    }

    cout << "\n  Name : " << currentName << endl;
    cout << "  ID   : " << currentId << endl;
    cout << "\n+----------------+" << endl;
    cout << "|     QUEUE      |" << endl; // 텍스트 변경
    cout << "+----------------+" << endl;

    for (int i = 0; i < (int)items.size(); i++) {
        if (i == 0)
            cout << "|  " << items[i] << " <- front (exit)" << endl;
        else if (i == (int)items.size() - 1)
            cout << "|  " << items[i] << " <- rear (entry)" << endl;
        else
            cout << "|  " << items[i] << endl;
    }

    if (items.empty())
        cout << "|  (empty)       |" << endl;
    cout << "+----------------+" << endl;
    cout << "  size: " << items.size() << endl;
}

void waitKey() {
    cout << "\n[Press Enter to continue...]" << endl;
    cin.clear(); // 입력 버퍼 비우기
    cin.ignore(100, '\n');
    cin.get(); // 엔터 입력 대기
    system("cls");
}
int main() {
    char cwd[1024];
    _getcwd(cwd, sizeof(cwd));
    cout << "현재 작업 경로: " << cwd << endl;

    SetConsoleOutputCP(65001);
    SetConsoleCP(65001);

    ifstream file("카페무솔트.csv");
    if (!file.is_open()) {
        cout << "File not found!" << endl;
        return 1;
    }

    string line;
    getline(file, line); // 헤더 건너뜀

    struct Person {
        string name, id, w1, w2, w3;
    };
    vector<Person> people;

    while (getline(file, line)) {
        stringstream ss(line);
        Person p;
        getline(ss, p.name, ',');
        getline(ss, p.id, ',');
        getline(ss, p.w1, ',');
        getline(ss, p.w2, ',');
        getline(ss, p.w3, ',');
        p.name = trim(p.name);
        p.id = trim(p.id);
        p.w1 = trim(p.w1);
        p.w2 = trim(p.w2);
        p.w3 = trim(p.w3);
        people.push_back(p);
    }
    file.close();

    queue<string> q; // queue 선언

    // 큐 선언 화면
    cout << "=== Queue Animation ===" << endl;
    cout << "Queue declared!" << endl;
    queue<string> emptyQ;
    printQueue(emptyQ, "-", "-");
    waitKey();

    // 사람별 애니메이션
    for (auto& p : people) {

        // push (enqueue) 3개
        vector<string> words = { p.w1, p.w2, p.w3 };
        for (auto& w : words) {
            cout << ">> queue.push(\"" << w << "\")" << endl;
            q.push(w);
            printQueue(q, p.name, p.id);
            waitKey();
        }

        // front 확인 (큐는 top 대신 front를 사용)
        cout << ">> queue.front() = \"" << q.front() << "\"" << endl;
        printQueue(q, p.name, p.id);
        waitKey();

        // pop (dequeue) 3개
        for (int i = 0; i < 3; i++) {
            cout << ">> queue.pop() -> removed: \"" << q.front() << "\"" << endl;
            q.pop();
            printQueue(q, p.name, p.id);
            waitKey();
        }
    }

    cout << "=== Done! Queue is empty ===" << endl;
    return 0;
}