const path = require('./path.js');


const ctx = canvas.getContext('2d');


const moveTo = (x, y) => {
  x *= coordWidth;
  x += offset.left;

  y *= coordHeight;
  y *= -1;
  y += offset.top;

  ctx.moveTo(x, y);
};

const lineTo = (x, y) => {
  x *= coordWidth;
  x += offset.left;

  y *= coordHeight;
  y *= -1;
  y += offset.top;

  ctx.lineTo(x, y)
};

const rect = (x, y, w, h) => {
  x *= coordWidth;
  x += offset.left;

  y *= coordHeight;
  y *= -1;
  y += offset.top;

  w *= coordWidth;
  h *= coordHeight;

  ctx.rect(x,y,w,h);
}

const circle = (x, y, r) => {
  x *= coordWidth;
  x += offset.left;

  y *= coordHeight;
  y *= -1;
  y += offset.top;

  ctx.arc(x, y, r, 0, 2 * Math.PI);
}






const changeColor = (newColor) => {
  if(ctx.strokeStyle !== newColor) {
    ctx.stroke();
    ctx.strokeStyle = newColor;
  }
};

const changeWidth = (newWidth) => {
  if(ctx.lineWidth !== newWidth) {
    ctx.stroke();
    ctx.lineWidth = newWidth
  }
};


path.forEach((node, i) => {
  if(i === 0) {
    moveTo(node.data.pos.x, node.data.pos.y);
  } else {
    lineTo(node.data.pos.x, node.data.pos.y);
  }  
});

ctx.lineWidth = 4;

ctx.strokeStyle = "#00F";
ctx.stroke();

saveImage();