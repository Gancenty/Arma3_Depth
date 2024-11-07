_laser_camera = 'camera' camCreate [0,0,0]; 
_laser_camera camSetFov 0.75; 
_laser_camera setPos (me modelToWorld [0, 0, 0]); 
_laser_camera cameraEffect ["Internal","Back"]; 
_laser_camera camCommit 0;
switchCamera _laser_camera;

arrow_list = [];
for "_i" from 1 to 100 do {
	arrow_list pushBack ("Sign_Arrow_F" createVehicle [0,0,0]);
};

onEachFrame { 
	for "_xi" from 0 to 9 do {
		for "_yi" from 0 to 9 do {
			_x_coord = -1 + _xi * 0.1;
			_y_coord = -1 + _yi * 0.1; 
			arrow = arrow_list select (_xi * 10 + _yi);
			_ins = lineIntersectsSurfaces [ 
				AGLToASL positionCameraToWorld [_x_coord,_y_coord,0], 
				AGLToASL positionCameraToWorld [_x_coord,_y_coord,100], 
				player, 
				objNull, 
				true, 
				1, 
				"PHYSX", 
				"GEOM" 
			]; 
			if (count _ins == 0) exitWith { arrow setPosASL [0,0,0] }; 
			arrow setPosASL (_ins select 0 select 0); 
			arrow setVectorUp (_ins select 0 select 1); 
		}
	};
};


wirefence = "Land_New_WiredFence_5m_F" createVehicle position player;
arrow = "Sign_Arrow_F" createVehicle [0,0,0];
onEachFrame {
	_ins = lineIntersectsSurfaces [
		AGLToASL positionCameraToWorld [0,0,0],
		AGLToASL positionCameraToWorld [0,0,1000],
		player,
		objNull,
		true,
		1,
		"GEOM",
		"NONE"
	];
	if (count _ins == 0) exitWith { arrow setPosASL [0,0,0] };
	arrow setPosASL (_ins select 0 select 0);
	arrow setVectorUp (_ins select 0 select 1);
	hintSilent str _ins;
};


///////////////////
private _cameraPos = getPosASL player; // 摄像机位置，假设在玩家位置  
private _horizontalFOV = 360;         // 水平视角（度）  
private _verticalFOV = 60;            // 垂直视角（度）  
private _angleResolution = 1;       // 角分辨率（度）  
private _maxDistance = 100;         
cnt = 0;
private _intersections = [];  

private _horizontalSteps = _horizontalFOV / _angleResolution;  
private _verticalSteps = _verticalFOV / _angleResolution;  

for "_i" from 0 to _horizontalSteps - 1 do {  
    private _horizontalAngle = (_i * _angleResolution) - (_horizontalFOV / 2);  
    for "_j" from 0 to _verticalSteps - 1 do {  
        private _verticalAngle = (_j * _angleResolution) - (_verticalFOV / 2);  

        private _dirX = cos (_horizontalAngle) * cos (_verticalAngle);  
        private _dirY = sin (_horizontalAngle) * cos (_verticalAngle);  
        private _dirZ = sin (_verticalAngle);  
        private _direction = [_dirX, _dirY, _dirZ];  

        private _endPos = _cameraPos vectorAdd (_direction vectorMultiply _maxDistance);  
        private _result = lineIntersectsSurfaces [_cameraPos, _endPos, player, objNull, true, 1, "PHYSX", "GEOM"];  
        if (!isNil "_result") then { 
			cnt = cnt+1; 
            private _intersectionPos = (_result select 0) select 0;  
            private _intersectionPosNorm = (_result select 0) select 1; 
			_point_info = [_intersectionPos, _intersectionPosNorm];  
            _intersections pushBack _point_info; 
        };
		if (count _intersections > 10) then { 
			["image.send_message", [_intersections]] call py3_fnc_callExtension; 
			_intersections = []; 
		};
	};  
}; 
if (count _intersections > 0) then { 
	["image.send_message", [_intersections]] call py3_fnc_callExtension; 
	_intersections = []; 
};
cnt
