#include "shapes.inc"

camera
{
    orthographic
    look_at <0, 0, 0>
    location <0, 0, 2.5>
}


union
{
light_source
{
   <-200, 400, 200> rgb <1,1,1> //rgb <2.2 2.25 2.25>
   area_light <250, 0, 0>, <0, 0, 250>, 3, 3  // 5, 5
   adaptive 1
   jitter
}

light_source
{
   <-200, 400, 200> rgb <.5,.5,.5> //rgb <2.2 2.25 2.25>
   area_light <250, 0, 0>, <0, 0, 250>, 100, 100  // 5, 5
   adaptive 1
   jitter
}

light_source
{
   <20, 20, 30> rgb <.25,.25,.25> //rgb <2.2 2.25 2.25>
   area_light <0, 8, 0>, <0, 0, 8>, 9, 3  // 5, 5
   adaptive 1
   jitter
}

light_source
{
   <40, 10, 5> rgb <.125,.125,.125> //rgb <2.2 2.25 2.25>
   area_light <0, 8, 0>, <0, 0, 8>, 9, 3  // 5, 5
   adaptive 1
   jitter
}

light_source
{
   <50, -5, -30> rgb <.05,.05,.05> //rgb <2.2 2.25 2.25>
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter
}

light_source
{
   <50, -5, -40> rgb <.05,.05,.05> //rgb <2.2 2.25 2.25>
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter
}

light_source
{
   <50, -5, -50> rgb <.05,.05,.05> //rgb <2.2 2.25 2.25>
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter
}

light_source
{
   <50, -5, -60> rgb <.05,.05,.05> //rgb <2.2 2.25 2.25>
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter
}

light_source
{
   <50, -5, -80> rgb <.05,.05,.05> //rgb <2.2 2.25 2.25>
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter
}

   rotate <30, 0, -45>
}
