import { a } from "./array.mjs";


let _g0 = 7;

function _f4(_p2, _p1, _p3, _p0) {
  for (let _g1 = _p1; _g1 < _p3; _g1++) {
    _p2[_g1] += _p0;
  }
}

function _f3(_p2, _p1, _p3, _p0) {
  for (let _g1 = _p1; _g1 < _p3; _g1++) {
    _p2[_g1] -= _p0;
  }
}

function _f2(_p2, _p1, _p3, _p0) {
  for (let _g1 = _p1; _g1 < _p3; _g1++) {
    _p2[_g1] ^= _p0;
  }
}

function _f1(_p1, _p0) {
  let _g2 = _p1[_p0 + 1];
  let _g3 = "";
  for (let _g4 = 0; _g4 < _g2; _g4++) {
    _g3 += String.fromCharCode(_p1[_p0 + 2 + _g4] ^ 0x37);
  }
  return _g3;
}

let _g5 = [_f4, _f3, _f2];

var map = new Map();

function _f0(_p1, _p0) {
  let _g6 = 0;
  while (_g6 < _p1.length) {
    let _g7 = _p1[_g6];

    if (_g7 == 5) {
      return _f1(_p1, _g6);
      break;
    }

    let _g8 = _p1[_g6 + 1];
    let _g9 = _p1[_g6 + 2];

    if (
      // (_p0[_g8] % _g9 == 0)==
      !(4 - _g7)
    ) {
      console.log(_g8,_g9)
      let temp = map.get(_g8);
      if (temp !== undefined) map.set(_g8, temp * _g9);
      else map.set(_g8, _g9);
      //   name[_g8] = _g9;
      //   _p0[_g8] = _g9;
      //   _g6 = _p1[_g6 + 3];
      //   continue;
    }

    _p0[_g8] = _p0[_g8] % _g9 ? _p0[_g8] : Math.floor(_p0[_g8] / _g9);
    let _ga = _p1[_g6 + 4];
    let _gb = _p1[_g6 + 5];
    let _gc = _p1[_g6 + 6] ^ (_g7 - 3);
    let _gd = _p1[_gc];
    _g5[_ga](_p1, _g6 + _g0, (_gb + 1) * _g0, _gd);
    _g6 += _g0;
  }
}

_f0(
  JSON.parse(JSON.stringify(a)),
  Array.from("name").map((x) => x.charCodeAt(0))
);

let word =  "";
for (let i = 0; i < map.size; i++) {
  word += String.fromCharCode(map.get(i));
}

console.log(word);
