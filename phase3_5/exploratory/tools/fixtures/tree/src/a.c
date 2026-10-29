static const iwad_t iwads[] =
{
    { "doom2.wad", 2 },
    //{ "strife0.wad", 9 },
    { "plutonia.wad", 3 },   /* not a row, { brace */
#ifdef HAVE_X
    { "x.wad", 4 },
#endif
    { "a,b{c}.wad", 5 },
};
const char *names[] = { "a", "b" };
int nums[3] = { 1, 2, 3 };
static char grid[2][3] = { {1,2,3}, {4,5,6} };
void (*fns[])(void) = { f, g };
static const cmd_t cmds[] = { { "x", f } };
void h(void) { int loc[] = { 1 }; }
static struct
{
    const char *description;
    int version;
} gameversions[] = {
    { "doom", 1 },
    { "ultimate", 2 },
    { NULL, 0 },
};
