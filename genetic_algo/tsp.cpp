// #include <SFML/Graphics.hpp>
#include <bits/stdc++.h>
#include <cmath>
#include <cstdio>
#include <cstdlib> // para rand()
#include <ctime>   // para time()
#include <limits.h>
#include <utility>
#include <vector>
using namespace std;

#define CITY_NUMBER 5
#define POP_SIZE 10
#define PARENTS 4
#define PROB_CROSSOVER 0.1

int id = 0;

struct individual {
  string gnome;
  double fitness;
};

struct city {
  int id;
  double x;
  double y;
};

// Função para gerar posições aleatórias
city generateCity(int x_max, int y_max) {
  city c;
  c.x = rand() % x_max; // posição x aleatória
  c.y = rand() % y_max; // posição y aleatória
  c.id = id++;
  return c;
}

void printCities(vector<struct city> cities) {
  for (auto c : cities) {
    cout << c.id << "\t(" << c.x << ", " << c.y << ")" << endl;
  }
}

double distance2cities(city a, city b) {
  return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2));
}

void calculateDistanceMap(double map[][CITY_NUMBER],
                          vector<struct city> cities) {
  for (int i = 0; i < CITY_NUMBER; i++) {
    for (int j = 0; j < CITY_NUMBER; j++) {
      map[i][j] = map[j][i] = distance2cities(cities[i], cities[j]);
    }
  }
}

void printMap(double map[][CITY_NUMBER]) {
  for (int i = 0; i < CITY_NUMBER; i++) {
    for (int j = 0; j < CITY_NUMBER; j++) {
      cout << std::setw(6) << std::fixed << std::setprecision(2) << map[i][j];
    }
    cout << endl;
  }
}

// Function to return a random number
// from start and end
int rand_num(int start, int end) {
  int r = end - start;
  int rnum = start + rand() % r;
  return rnum;
}

// Function to check if the character
// has already occurred in the string
bool repeat(string s, char ch) {
  for (int i = 0; i < s.size(); i++) {
    if (s[i] == ch)
      return true;
  }
  return false;
}

// Function to return the updated value
// of the cooling element.
int cooldown(int temp) { return (90 * temp) / 100; }

// Function to return a mutated GNOME
// Mutated GNOME is a string
// with a random interchange
// of two genes to create variation in species
string mutatedGene(string gnome) {
  while (true) {
    int r = rand_num(1, CITY_NUMBER);
    int r1 = rand_num(1, CITY_NUMBER);
    if (r1 != r) {
      char temp = gnome[r];
      gnome[r] = gnome[r1];
      gnome[r1] = temp;
      break;
    }
  }
  return gnome;
}

void selectParents(individual individuals[], individual selected[PARENTS]) {
  int sel = 0;
  while (sel < PARENTS) {
    int i = rand_num(0, POP_SIZE);
    if (individuals[i].fitness > rand()) {
      selected[sel] = individuals[i];
      sel++;
    }
  }
}

// Function to return a valid GNOME string
// required to create the population
string create_gnome() {
  string gnome = "0";
  while (true) {
    if (gnome.size() == CITY_NUMBER) {
      gnome += gnome[0];
      break;
    }
    int temp = rand_num(1, CITY_NUMBER);
    if (!repeat(gnome, (char)(temp + 48)))
      gnome += (char)(temp + 48);
  }
  return gnome;
}

// Function to return the fitness value of a gnome.
// The fitness value is the path length
// of the path represented by the GNOME.
double cal_fitness(string gnome, double map[][CITY_NUMBER]) {
  double f = 0;
  for (int i = 0; i < gnome.size() - 1; i++) {
    f += map[gnome[i] - 48][gnome[i + 1] - 48];
  }
  return f;
}

// Comparator for GNOME struct.
bool lessthan(struct individual t1, struct individual t2) {
  return t1.fitness < t2.fitness;
}

individual crossover(individual p1, individual p2) {
  individual child;
  int start = rand_num(0, CITY_NUMBER + 1);
  int end = rand_num(0, CITY_NUMBER + 1);

  if (start < end)
    swap(end, start);

  child.gnome = create_gnome();
  for (int j = start; j < end; j++) {
    child.gnome[j] = p1.gnome[j];
  }

  int pointer = 0;
  for (int j = 0; j < CITY_NUMBER + 1; j++) {
    if (child.gnome[j] == '0') {
      while (find(child.gnome.begin(), child.gnome.end(), p2.gnome[pointer]) !=
             child.gnome.end())
        pointer++;
      child.gnome[j] = p2.gnome[pointer];
    }
  }
  return child;
}

int main() {

  // Inicializa o gerador de números aleatórios
  srand(42);
  int x_max = 10;
  int y_max = 10;

  vector<struct city> cities;
  struct city origin;
  origin.id = id++;
  origin.x = x_max / 2;
  origin.y = y_max / 2;
  cities.push_back(origin);

  // Populating the GNOME pool.
  for (int i = 0; i < CITY_NUMBER; i++) {
    cities.push_back(generateCity(x_max, y_max));
  }

  printCities(cities);
  double map[CITY_NUMBER][CITY_NUMBER];
  calculateDistanceMap(map, cities);
  printMap(map);

  // Generation Number
  int gen = 1;
  // Number of Gene Iterations
  int gen_thres = 5;
  vector<struct individual> population;

  struct individual temp;

  // Populating the GNOME pool.
  for (int i = 0; i < POP_SIZE; i++) {
    temp.gnome = create_gnome();
    temp.fitness = cal_fitness(temp.gnome, map);
    population.push_back(temp);
  }

  cout << "\nInitial population: " << endl << "GNOME\tFITNESS VALUE\n";
  for (int i = 0; i < POP_SIZE; i++)
    cout << population[i].gnome << "\t" << population[i].fitness << endl;
  cout << "\n";

  for (int i = 0; i < 5; i++) {
    individual temp = crossover(population[0], population[1]);
    cout << temp.gnome << endl;
  }

  return 0;
}
