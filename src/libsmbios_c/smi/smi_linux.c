/* -*- Mode: C; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*-
 * vim:expandtab:autoindent:tabstop=4:shiftwidth=4:filetype=c:cindent:textwidth=0:
 *
 * Copyright (C) 2005 Dell Inc.
 *  by Michael Brown <Michael_E_Brown@dell.com>
 * Licensed under the Open Software License version 2.1
 *
 * Alternatively, you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published
 * by the Free Software Foundation; either version 2 of the License,
 * or (at your option) any later version.

 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 */

#define LIBSMBIOS_C_SOURCE

// Include compat.h first, then system headers, then public, then private
#include "smbios_c/compat.h"

// system
#include <stdlib.h>
#include <string.h>

// public
#include "smbios_c/obj/smi.h"
#include "smbios_c/types.h"

// private
#include "smi_impl.h"

// forward declarations

int __internal LINUX_dell_smi_obj_execute(struct dell_smi_obj *this)
{
    fnprintf("FOO!\n");
    return -1;
}

void __internal init_dell_smi_obj(struct dell_smi_obj *this)
{
    this->execute = LINUX_dell_smi_obj_execute;
}
