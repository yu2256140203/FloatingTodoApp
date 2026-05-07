/**
 * 图标生成脚本
 * 运行此脚本可自动生成应用图标
 *
 * 使用方法：
 * 1. 安装canvas依赖：npm install canvas
 * 2. 运行脚本：node generate-icon.js
 */

const { createCanvas } = require('canvas');
const fs = require('fs');

// 创建256x256的画布
const size = 256;
const canvas = createCanvas(size, size);
const ctx = canvas.getContext('2d');

// 绘制圆角矩形
function roundRect(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

// 创建渐变背景
const gradient = ctx.createLinearGradient(0, 0, size, size);
gradient.addColorStop(0, '#667eea');
gradient.addColorStop(1, '#764ba2');

// 绘制背景
roundRect(0, 0, size, size, 40);
ctx.fillStyle = gradient;
ctx.fill();

// 绘制勾选标记
ctx.strokeStyle = 'white';
ctx.lineWidth = 16;
ctx.lineCap = 'round';
ctx.lineJoin = 'round';

ctx.beginPath();
ctx.moveTo(70, 130);
ctx.lineTo(110, 170);
ctx.lineTo(190, 90);
ctx.stroke();

// 保存为PNG
const buffer = canvas.toBuffer('image/png');
fs.writeFileSync('icon.png', buffer);

console.log('图标已生成：icon.png');
