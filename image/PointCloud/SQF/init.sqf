_start_scan = false;
_new_mission = [];
_target_pos = [0, 0, 0];
_target_control = [0, 0, 0];

object_class_map = createHashMap;
next_class_num = 0;


fuc_low_scan = {
	params ["_center"];
	private _cameraPos = _center; 		  // 摄像机位置 
	private _horizontalFOV = 360;         // 水平视角（度）   
	private _verticalFOV = 180;            // 垂直视角（度）   
	private _angleResolution = 0.2;       // 角分辨率（度）   
	private _maxDistance = 100;          
	private _points_cnt = 0; 
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
			
			_point_info = [];
			_point_class_str = "";
			_point_class = 0;
			_min_points_info = [];
			_min_distance = 999999;
			
			private _result_fire = lineIntersectsSurfaces [_cameraPos, _endPos, player, objNull, true, 1, "VIEW", "FIRE"];
			if (count _result_fire > 0) then {
				private _intersectionPos = (_result_fire select 0) select 0;   
				private _intersectionPosNorm = (_result_fire select 0) select 1; 
				private _intersectionClass = (_result_fire select 0) select 2;
				_point_class_str = str _intersectionClass;
				
				if (_point_class_str in object_class_map) then {
					_point_class = object_class_map get _point_class_str;
				} else {
					_point_class = next_class_num;
					object_class_map set [_point_class_str, next_class_num];
					next_class_num = next_class_num + 1;
				};

				_point_info = [_intersectionPos select 0, _intersectionPos select 1, _intersectionPos select 2, _intersectionPosNorm select 0, _intersectionPosNorm select 1,_intersectionPosNorm select 2, _point_class];
				_distance = _cameraPos vectorDistance _intersectionPos;
				if (_distance < _min_distance) then {
					_min_distance = _distance;
					_min_points_info = _point_info;
				};
			}; 
			

			private _result_geom = lineIntersectsSurfaces [_cameraPos, _endPos, player, objNull, true, 1, "GEOM", "NONE"];   
			if (count _result_geom > 0) then {
				private _intersectionPos = (_result_geom select 0) select 0;   
				private _intersectionPosNorm = (_result_geom select 0) select 1; 
				private _intersectionClass = (_result_geom select 0) select 2;
				_point_class_str = str _intersectionClass;

				if (_point_class_str in object_class_map) then {
					_point_class = object_class_map get _point_class_str;
				} else {
					_point_class = next_class_num;
					object_class_map set [_point_class_str, next_class_num];
					next_class_num = next_class_num + 1;
				};

				_point_info = [_intersectionPos select 0, _intersectionPos select 1, _intersectionPos select 2, _intersectionPosNorm select 0, _intersectionPosNorm select 1,_intersectionPosNorm select 2, _point_class];
				_distance = _cameraPos vectorDistance _intersectionPos;
				if (_distance < _min_distance) then {
					_min_distance = _distance;
					_min_points_info = _point_info;
				};
			};
			
			if (count _min_points_info > 0)  then { 
				_points_cnt = _points_cnt + 1;   
				_intersections pushBack _min_points_info;  
			}; 
			if (count _intersections > 100000) then {  
				["image.send_message", [_intersections]] call py3_fnc_callExtension;  
				_intersections = [];  
			}; 
		};   
	};  
	if (count _intersections > 0) then {  
		["image.send_message", [_intersections]] call py3_fnc_callExtension;  
		_intersections = [];  
	};
	_points_cnt
};


fuc_high_scan = {
	params ["_center"];
	private _cameraPos = _center; 		  // 摄像机位置 
	private _horizontalFOV = 360;         // 水平视角（度）   
	private _verticalFOV = 45;            // 垂直视角（度）   
	private _angleResolution = 0.2;       // 角分辨率（度）   
	private _maxDistance = 100;          
	private _points_cnt = 0; 
	private _intersections = [];   
	
	private _horizontalSteps = _horizontalFOV / _angleResolution;   
	private _verticalSteps = _verticalFOV / _angleResolution;   
	
	for "_i" from 0 to _horizontalSteps - 1 do {   
		private _horizontalAngle = (_i * _angleResolution) - (_horizontalFOV / 2);   
		for "_j" from 0 to _verticalSteps - 1 do {   
			private _verticalAngle = -90 + (_j * _angleResolution);   
			
			private _dirX = cos (_horizontalAngle) * cos (_verticalAngle);   
			private _dirY = sin (_horizontalAngle) * cos (_verticalAngle);   
			private _dirZ = sin (_verticalAngle);   
			private _direction = [_dirX, _dirY, _dirZ];   
			private _endPos = _cameraPos vectorAdd (_direction vectorMultiply _maxDistance); 
			
			_point_info = [];
			_point_class_str = "";
			_point_class = 0;
			_min_points_info = [];
			_min_distance = 999999;
			
			private _result_fire = lineIntersectsSurfaces [_cameraPos, _endPos, player, objNull, true, 1, "VIEW", "FIRE"];
			if (count _result_fire > 0) then {
				private _intersectionPos = (_result_fire select 0) select 0;   
				private _intersectionPosNorm = (_result_fire select 0) select 1; 
				private _intersectionClass = (_result_fire select 0) select 2;
				_point_class_str = str _intersectionClass;

				if (_point_class_str in object_class_map) then {
					_point_class = object_class_map get _point_class_str;
				} else {
					_point_class = next_class_num;
					object_class_map set [_point_class_str, next_class_num];
					next_class_num = next_class_num + 1;
				};

				_point_info = [_intersectionPos select 0, _intersectionPos select 1, _intersectionPos select 2, _intersectionPosNorm select 0, _intersectionPosNorm select 1,_intersectionPosNorm select 2, _point_class];
				_distance = _cameraPos vectorDistance _intersectionPos;
				if (_distance < _min_distance) then {
					_min_distance = _distance;
					_min_points_info = _point_info;
				};
			}; 
			

			private _result_geom = lineIntersectsSurfaces [_cameraPos, _endPos, player, objNull, true, 1, "GEOM", "NONE"];   
			if (count _result_geom > 0) then {
				private _intersectionPos = (_result_geom select 0) select 0;   
				private _intersectionPosNorm = (_result_geom select 0) select 1; 
				private _intersectionClass = (_result_geom select 0) select 2;
				_point_class_str = str _intersectionClass;

				if (_point_class_str in object_class_map) then {
					_point_class = object_class_map get _point_class_str;
				} else {
					_point_class = next_class_num;
					object_class_map set [_point_class_str, next_class_num];
					next_class_num = next_class_num + 1;
				};

				_point_info = [_intersectionPos select 0, _intersectionPos select 1, _intersectionPos select 2, _intersectionPosNorm select 0, _intersectionPosNorm select 1,_intersectionPosNorm select 2, _point_class];
				_distance = _cameraPos vectorDistance _intersectionPos;
				if (_distance < _min_distance) then {
					_min_distance = _distance;
					_min_points_info = _point_info;
				};
			};
			
			if (count _min_points_info > 0)  then { 
				_points_cnt = _points_cnt + 1;   
				_intersections pushBack _min_points_info;  
			}; 
			if (count _intersections > 100000) then {  
				["image.send_message", [_intersections]] call py3_fnc_callExtension;  
				_intersections = [];  
			}; 
		};   
	};  
	if (count _intersections > 0) then {  
		["image.send_message", [_intersections]] call py3_fnc_callExtension;  
		_intersections = [];  
	};
	_points_cnt
};


while {true} do {
	_new_mission = ["image.read_message", []] call py3_fnc_callExtension;
	if (_new_mission select 0 == "Y") then {
		_target_control = _new_mission select 1;
		_target_pos = ATLToASL([_target_control select 0, _target_control select 1, 3]);
		_start_scan = true;
	};
	if (_start_scan) then {
		_start_scan = false;

		_target_pos = ATLToASL([_target_control select 0, _target_control select 1, 3]);
		_cnt1 = [_target_pos] call fuc_low_scan;
		sleep(0.1);

		_target_pos = ATLToASL([_target_control select 0, _target_control select 1, 20]);
		_cnt2 = [_target_pos] call fuc_high_scan;
		sleep(0.1);

		["image.send_com_message", ["Y"+str (_cnt1 + _cnt2)]] call py3_fnc_callExtension;
		["image.send_com_message", ["I"+str (object_class_map)]] call py3_fnc_callExtension;
	};
	sleep(0.001);
};