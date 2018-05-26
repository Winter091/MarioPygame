<?xml version="1.0" encoding="UTF-8"?>
<tileset name="tiles" tilewidth="32" tileheight="32" tilecount="39" columns="13">
 <image source="tiles.png" width="416" height="96"/>
 <tile id="0" type="gnd_red"/>
 <tile id="1" type="stair"/>
 <tile id="2" type="brick"/>
 <tile id="3" type="q_0">
  <animation>
   <frame tileid="3" duration="500"/>
   <frame tileid="4" duration="100"/>
   <frame tileid="5" duration="100"/>
   <frame tileid="4" duration="100"/>
  </animation>
 </tile>
 <tile id="4" type="q_1"/>
 <tile id="5" type="q_2"/>
 <tile id="6" type="q_activated"/>
 <tile id="7" type="cloud_bot"/>
 <tile id="8" type="cloud_top"/>
</tileset>
