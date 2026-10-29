#include <string.h>
#include "i_system.h"

/* the valid modes a player may ask for */
static const struct {
    const char *name;
    int n;
} valid_modes[] = {
    { "easy", 1 },
    { "hard", 2 },
    { NULL, 0 }
};

int lookup_mode(const char *s)
{
    int i;
    for (i = 0; valid_modes[i].name; i++)
    {
        if (!strcmp(valid_modes[i].name, s))
            return valid_modes[i].n;
    }
    I_Error("unknown mode %s", s);
    return -1;
}
