/* 
 * Case for Raspberry Pi Pico with built in cable retainer
 *
 * Design: hxr.social/@thomasflummer
 *
 * License: CC-BY-SA
 *
 */
 
module case_bottom(pcb_length, pcb_width)
{
    difference()
    {
        union()
        {
            hull()
            {
                // main case
                hull()
                {
                    for (x = [-1, 1])
                    {
                        for (y = [-1, 1])
                        {
                            translate([x*((pcb_length+2)/2 - 4), y*((pcb_width+4+12)/2 - 4), 2+5/2])
                                cylinder(h = 5, r = 4, center = true, $fn = 80);
                        }
                    }
                }

                // bottom chamfer
                hull()
                {
                    for (x = [-1, 1])
                    {
                        for (y = [-1, 1])
                        {
                            translate([x*((pcb_length+2)/2 - 4), y*((pcb_width+4+12)/2 - 4), 2/2])
                                cylinder(h = 2, r = 2, center = true, $fn = 80);
                        }
                    }
                }
            }
        }
        union()
        {
            // pcb
            translate([0, 0, 5+2-1.2/2])
                cube([pcb_length, pcb_width, 1.21], center = true);

            // micro USB cutout
            translate([pcb_length/2, 0, 5+2-0.5/2])
                cube([10, 8.5, 0.51], center = true);

            translate([0, 0, 5+2-4/2])
                cube([pcb_length-5, pcb_width, 8.01], center = true);

            translate([0, 0, 5+2-4/2])
                cube([pcb_length-16, pcb_width+12, 8.01], center = true);

            // cutout for inserts
            for (x = [-1, 1])
            {
                for (y = [-1, 1])
                {
                    translate([x*((pcb_length+2)/2 - 4), y*((pcb_width+4+12)/2 - 4), 2+5/2])
                        cylinder(h = 5.01, d = 4, center = true, $fn = 80);
                }
            }        
        }
    }
}

module case_top(pcb_length, pcb_width, height)
{
    difference()
    {
        union()
        {
            hull()
            {
                // main case
                hull()
                {
                    for (x = [-1, 1])
                    {
                        for (y = [-1, 1])
                        {
                            translate([x*((pcb_length+2)/2 - 4), y*((pcb_width+4+12)/2 - 4), height/2])
                                cylinder(h = height, r = 4, center = true, $fn = 80);
                        }
                    }
                }

                // top chamfer
                hull()
                {
                    for (x = [-1, 1])
                    {
                        for (y = [-1, 1])
                        {
                            translate([x*((pcb_length+2)/2 - 4), y*((pcb_width+4+12)/2 - 4), height+2/2])
                                cylinder(h = 2, r = 2, center = true, $fn = 80);
                        }
                    }
                }
            }
        }
        union()
        {
            translate([12/2, 0, (height)/2])
                cube([pcb_length-5-12, pcb_width-2, height+0.01], center = true);

            translate([6/2, 0, (height)/2])
                cube([pcb_length-16-6, pcb_width+12, height+0.01], center = true);

            // micro USB cutout
            translate([pcb_length/2, 0, 2.9/2])
                cube([10, 8.5, 2.91], center = true);
                
            // cable cutout
            translate([-pcb_length/2, 0, 6/2])
            rotate(90, [0, 1, 0])
                cylinder(h = 10, d = 5.5, center = true, $fn = 80);

            translate([-pcb_length/2, 0, 3/2])
                cube([10, 5.5, 3.01], center = true);

            // cable support
            difference()
            {
                translate([0, 0, (height)/2])
                    cube([pcb_length-5, 10, height+0.01], center = true);

                translate([-pcb_length/2+6, -6, (height)/2])
                    cube([2, 10, height+1], center = true);

                translate([-pcb_length/2+13, 6, (height)/2])
                    cube([2, 10, height+1], center = true);
            }
            
            // cutout for screws
            for (x = [-1, 1])
            {
                for (y = [-1, 1])
                {
                    translate([x*((pcb_length+2)/2 - 4), y*((pcb_width+4+12)/2 - 4), height/2])
                        cylinder(h = height+10, d = 3.3, center = true, $fn = 30);

                    translate([x*((pcb_length+2)/2 - 4), y*((pcb_width+4+12)/2 - 4), height+4/2-1.4])
                        cylinder(h = 4, d = 7, center = true, $fn = 60);

                    translate([x*((pcb_length+2)/2 - 4), y*((pcb_width+4+12)/2 - 4 + 7/2), height+4/2-1.4])
                        cube([7, 7, 4], center = true);

                    translate([x*((pcb_length+2)/2 - 4 + 7/2), y*((pcb_width+4+12)/2 - 4), height+4/2-1.4])
                        cube([7, 7, 4], center = true);
                }
            }
                
        }
    }
}


difference()
{
    union()
    {

//        color("#666666")
//        translate([0, 0, 0])
//            case_top(52, 21.5, 7);

        color("#666666")
        translate([0, 0, -2-5])
            case_bottom(82, 72.5);

    }
    union()
    {
        //rotate(30, [0, 0, 1])
        //translate([0, 50, 0])
        //   cube([100, 100, 100], center = true);
    }
}
/*
color("#cccccc")
translate([-51.3/2, 21/2, -1])
rotate(-90, [0, 0, 1])
    import("pico.stl");
*/

