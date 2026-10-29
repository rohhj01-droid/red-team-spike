static void f(void) {}
static void g(void) {}

static const int sine_table[] = {
    0, 1, 2, 3
};

static void (*dispatch[])(void) = {
    f,
    g
};
