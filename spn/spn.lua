require "grundl"
require "krypto"
require "analyse"

local transvl = 
    {1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12 , 16}
local sboxaufg = sboxHex("E213D906F45A8C7B")
local spnvl = spn(16,kgenShift,sboxaufg,4,transvl,4)
local kspnvl = hexStringToBitArray("4AA4")
local xspnvl = hexStringToBitArray("26B7")

file = io.open("keys.txt", "w")
local i=0
for j=0,65536 do
  for k=0,65536 do
    --we are using the x-differential from excercise 41
    -- x' = int(1001 0000 0000 1001,2) == 36873
     if ((j ~ k) == 36873) then
       x=intToBitArray(j,16)
       x_star=intToBitArray(k,16)
       y=bitArrayToHexString(spnvl(xspnvl,x))
       y_star=bitArrayToHexString(spnvl(xspnvl,x_star))
       x=bitArrayToHexString(x)
       x_star=bitArrayToHexString(x_star)
       file:write(x , ',' , x_star , ',' , y , ',' , y_star,'\n')
       i=i+1
     end
   end
   if (i >= 1700) then
     break
   end
 end
