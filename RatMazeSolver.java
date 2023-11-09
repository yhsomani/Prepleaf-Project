package Prepleaf;
import java.util.ArrayDeque;
import java.util.Queue;
import java.util.Random;
import java.util.Scanner;

public class RatMazeSolver {
    static int n = 10; // Adjust the size of the maze (n x n) as needed

    public static void main(String[] args) {
        while (true) {
            char[][] maze = generateMaze(n);
            System.out.println();
            System.out.println("Options:");
            System.out.println("0. to Enter Size of Maze");
            System.out.println("1. Print Shortest Path");
            System.out.println("2. Generate Another Maze");
            System.out.println("3. Exit");
            System.out.print("Select an option: ");

            int option = getUserOption();
            if (option == 1) {
                char[][] pathMaze = findShortestPath(maze);
                printMaze(pathMaze);
            } else if (option == 2) {
                printMaze(maze);
            } else if (option == 3) {
                System.out.println("Exiting Maze Solver. Goodbye!");
                break;
            } else if (option == 0) {
                // Input to change maze size, you can implement this functionality
            } else {
                System.out.println("Invalid option. Please try again.");
            }
        }
    }

    private static int getUserOption() {
        Scanner sc = new Scanner(System.in);
        int option = sc.nextInt();
        sc.nextLine(); // Consume the newline character
        if (option == 0) {
            System.out.print("Enter the Size of Maze (n x n): ");
            n = sc.nextInt();
        }
        return option;
    }

    private static char[][] generateMaze(int n) {
        char[][] maze = new char[n][n];
        int wallPercentage = 25;

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (i == 0 && j == 0) {
                    maze[i][j] = 'S'; // Start
                } else if (i == n - 1 && j == n - 1) {
                    maze[i][j] = 'E'; // End
                } else if (new Random().nextInt(100) < wallPercentage) {
                    maze[i][j] = '|'; // Wall
                } else {
                    maze[i][j] = '-'; // Open Space
                }
            }
        }

        return maze;
    }

    private static void printMaze(char[][] maze) {
        for (char[] row : maze) {
            for (char cell : row) {
                System.out.print(cell + " ");
            }
            System.out.println();
        }
    }

    private static char[][] findShortestPath(char[][] maze) {
        int n = maze.length;
        char[][] pathMaze = new char[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                pathMaze[i][j] = maze[i][j];
            }
        }

        int[] dx = {0, 1, 0, -1};
        int[] dy = {-1, 0, 1, 0};
        int[][] distance = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                distance[i][j] = Integer.MAX_VALUE;
            }
        }

        Queue<Integer> queue = new ArrayDeque<>();
        int start = 0;
        int end = n * n - 1;

        queue.add(start);
        distance[start / n][start % n] = 0;

        while (!queue.isEmpty()) {
            int current = queue.poll();
            int curX = current / n;
            int curY = current % n;

            if (current == end) {
                break;
            }

            for (int dir = 0; dir < 4; dir++) {
                int nextX = curX + dx[dir];
                int nextY = curY + dy[dir];

                if (nextX >= 0 && nextX < n && nextY >= 0 && nextY < n
                        && maze[nextX][nextY] != '|' && distance[nextX][nextY] == Integer.MAX_VALUE) {
                    queue.add(nextX * n + nextY);
                    distance[nextX][nextY] = distance[curX][curY] + 1;
                }
            }
        }

        int current = end;
        while (current != start) {
            int curX = current / n;
            int curY = current % n;
            pathMaze[curX][curY] = 'o'; // Mark the shortest path
            for (int dir = 0; dir < 4; dir++) {
                int nextX = curX + dx[dir];
                int nextY = curY + dy[dir];
                if (nextX >= 0 && nextX < n && nextY >= 0 && nextY < n
                        && distance[nextX][nextY] == distance[curX][curY] - 1) {
                    current = nextX * n + nextY;
                    break;
                }
            }
        }

        return pathMaze;
    }
}
 
