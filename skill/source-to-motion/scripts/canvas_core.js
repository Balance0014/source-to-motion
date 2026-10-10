// Small drawing primitives shared by authored browser scenes. No layout template.
const M = (() => {
  const clamp = (v, a=0, b=1) => Math.max(a, Math.min(b, v));
  const ease = v => { v=clamp(v); return v*v*(3-2*v); };
  const phase = (t,a,b) => ease((t-a)/(b-a));
  const rgba = (rgb,a=1) => `rgba(${rgb[0]},${rgb[1]},${rgb[2]},${clamp(a)})`;
  const rnd = seed => () => { seed = (seed*1664525+1013904223)>>>0; return seed/4294967296; };
  const glowSprites=new Map();
  function text(ctx,s,x,y,size=28,color='#fff',weight=600,align='left',alpha=1) {
    ctx.save(); ctx.globalAlpha=clamp(alpha); ctx.fillStyle=color;
    ctx.textAlign=align; ctx.textBaseline='middle';
    ctx.font=`${weight} ${size}px Space Grotesk, Arial, sans-serif`;
    ctx.fillText(String(s),x,y); ctx.restore();
  }
  function glow(ctx,x,y,r,color,power=1) {
    const key=color.join(',');
    let sprite=glowSprites.get(key);
    if(!sprite){
      sprite=document.createElement('canvas');sprite.width=128;sprite.height=128;
      const sc=sprite.getContext('2d');
      const g=sc.createRadialGradient(64,64,0,64,64,64);
      g.addColorStop(0,rgba(color,.32));g.addColorStop(.25,rgba(color,.13));g.addColorStop(1,rgba(color,0));
      sc.fillStyle=g;sc.fillRect(0,0,128,128);glowSprites.set(key,sprite);
    }
    ctx.save();ctx.globalAlpha*=clamp(power);ctx.drawImage(sprite,x-r,y-r,2*r,2*r);ctx.restore();
  }
  function line(ctx,x1,y1,x2,y2,color,width=2,alpha=1) {
    ctx.strokeStyle=rgba(color,alpha); ctx.lineWidth=width;
    ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
  }
  function dot(ctx,x,y,r,color,alpha=1) {
    ctx.fillStyle=rgba(color,alpha);ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();
  }
  function box(ctx,x,y,w,h,fill,stroke=null,r=12,sw=1) {
    ctx.beginPath();ctx.roundRect(x,y,w,h,r);
    if(fill){ctx.fillStyle=fill;ctx.fill();}
    if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=sw;ctx.stroke();}
  }
  function vignette(ctx,w,h,power=.7) {
    const g=ctx.createRadialGradient(w*.48,h*.45,h*.08,w*.48,h*.45,h*.75);
    g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(1,`rgba(0,0,0,${power})`);
    ctx.fillStyle=g;ctx.fillRect(0,0,w,h);
  }
  function cover(ctx,img,w,h,zoom=1,xoff=0,yoff=0) {
    const k=Math.max(w/img.width,h/img.height)*zoom;
    const dw=img.width*k,dh=img.height*k;
    ctx.drawImage(img,(w-dw)/2+xoff,(h-dh)/2+yoff,dw,dh);
  }
  return {clamp,ease,phase,rgba,rnd,text,glow,line,dot,box,vignette,cover};
})();
