#include <windows.h>
#include <conio.h>
#include <stdio.h>

int main() {
    int hx = 0, hy = 0;
    int len = 4;
    int map[900] = {0};
    int i = 0;
    char c = 'd', cl = 'd';
    char deaw[1801];
    system("mode con:cols=60 lines=30");
    srand((unsigned)malloc(1));
    // map[i], 1:snake, 0:window, -1:food
    map[rand() % 900] = -1;
    while (1) {
        if (_kbhit()) {  // 按键检测
            cl = _getch();  // 获取一个字符
            if ((cl == 'a' && c != 'd') || (cl == 'd' && c != 'a') ||
                    (cl == 'w' && c != 's') || (cl == 's' && c != 'w')) {
                c = cl;
            }
        }
        if ((c == 'a' && --hx < 0) || (c == 'd' && ++hx == 30) ||
                (c == 'w' && --hy < 0) || (c == 's' && ++hy == 30)) {
            break;
        }
        if (map[hy*30 + hx] < 0) {
            len++;
            i = rand() % 900;
            while (map[i] != 0) {
                i = rand() % 900;
            }
            map[i] = -1;
        }
        else {
            for (i = 0; i < 900; ++i) {
                if (map[i] > 0) {
                    map[i]--;
                }
            }
        }
        map[hy*30 + hx] = len;
        system("cls");
        for (i = 0; i < 900; ++i) {
            if (map[i] < 0) {
                deaw[i*2] = '0';
                deaw[i*2+1] = '0';
            }
            else if (map[i] == 0) {
                deaw[i*2] = ' ';
                deaw[i*2+1] = ' ';
            }
            else {
                deaw[i*2] = '(';
                deaw[i*2+1] = ')';
            }
        }
        printf(deaw);
        Sleep(100);
    }
}
