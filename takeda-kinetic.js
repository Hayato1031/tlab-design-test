(() => {
  'use strict';
  const reduce=matchMedia('(prefers-reduced-motion: reduce)');
  const english=document.documentElement.lang==='en';
  const root=document.querySelector('.kinetic');
  if(root){
  const topics=[
    {id:'media',name:english?'Media art':'メディア',sub:english?'Light, sound and spatial expression':'光・音響・空間への表現',color:'#307db1'},
    {id:'video',name:english?'Film / Video':'動画・映像',sub:english?'Filming, editing and motion graphics':'撮影・編集・モーショングラフィックス',color:'#387a68'},
    {id:'cg',name:english?'Computer graphics':'CG',sub:english?'3D graphics, animation and visual expression':'3DCG・アニメーション・映像表現',color:'#537bb3'},
    {id:'ai',name:english?'Generative AI':'生成AI',sub:english?'Video production and new approaches to problems':'映像制作・新しい問題解決の手法',color:'#7864b7'},
    {id:'drone',name:english?'Drones / UAV':'ドローン',sub:english?'Development, control and flight testing':'機体開発・制御・飛行試験',color:'#3b7185'},
    {id:'xr',name:english?'Extended reality':'VR / AR / XR',sub:english?'Experiences and application development':'体験設計・アプリケーション開発',color:'#a2608e'}
  ];
  const words=[...root.querySelectorAll('.word')],photos=[...root.querySelectorAll('[data-photo]')];
  const title=root.querySelector('[data-caption-title]'),subtitle=root.querySelector('[data-caption-sub]');
  const preview=new URLSearchParams(location.search),staticPreview=preview.get('motion')==='off';
  const startIndex=Math.max(0,topics.findIndex(t=>t.id===preview.get('theme')));
  let index=0,elapsed=0,last=0,raf=0,clock=0,drawAt=0,visible=true;
  const duration=5800;
  const canvas=root.querySelector('canvas'),ctx=canvas?.getContext('2d');let width=0,height=0;
  function draw(){
    if(!ctx||!width||!height)return;ctx.clearRect(0,0,width,height);
    const small=width<620,scale=Math.min(width*(small?.52:.31),height*.64),cx=width*.53,cy=height*.48,turn=clock*.13;
    const palette=['#4b7cd2','#288bbd','#4aaabb','#9c80c4','#d477aa','#dd9386'];
    for(let row=0;row<51;row++){
      const v=row/50*Math.PI*2;ctx.fillStyle=palette[Math.floor(row/9+index)%palette.length];
      for(let col=0;col<112;col++){
        const u=col/112*Math.PI*2;
        const r=.78+.23*Math.cos(v)+.12*Math.sin(u*3+turn+index*.5);
        const x=r*Math.cos(u),y=r*Math.sin(u),z=.42*Math.sin(v+u*2+turn*.3);
        const xx=x*Math.cos(turn)-y*Math.sin(turn),yy=x*Math.sin(turn)+y*Math.cos(turn);
        const px=cx+xx*scale*1.32,py=cy+(yy*.46-z*.84)*scale;
        const depth=(yy+1.4)/2.8;ctx.globalAlpha=.4+depth*.42;
        const dot=(small?.8:1.05)+depth*1.15;
        ctx.fillRect(px,py,dot,dot);
      }
    }
    ctx.globalAlpha=1;
  }
  function resize(){if(!ctx)return;const r=canvas.getBoundingClientRect();width=r.width;height=r.height;const ratio=Math.min(devicePixelRatio||1,2);canvas.width=Math.round(width*ratio);canvas.height=Math.round(height*ratio);ctx.setTransform(ratio,0,0,ratio,0,0);draw();}
  function show(next){
    const old=index;index=(next+topics.length)%topics.length;const topic=topics[index];elapsed=0;
    root.dataset.topic=topic.id;root.style.setProperty('--theme',topic.color);
    words.forEach((word,i)=>{word.classList.toggle('active',i===index);word.classList.toggle('leaving',i===old&&old!==index);word.setAttribute('aria-hidden',String(i!==index));});
    photos.forEach(p=>p.classList.toggle('active',p.dataset.photo===topic.id));
    title.textContent=topic.name;subtitle.textContent=topic.sub;draw();
  }
  function stopped(){return staticPreview||reduce.matches||document.hidden||!visible;}
  function tick(now){raf=0;if(stopped())return;const dt=last?Math.min(now-last,70):0;last=now;elapsed+=dt;clock+=dt/1000;if(elapsed>=duration)show(index+1);if(now-drawAt>40){draw();drawAt=now;}raf=requestAnimationFrame(tick);}
  function sync(){root.classList.toggle('motion-paused',stopped());if(stopped()){cancelAnimationFrame(raf);raf=0;last=0;}else if(!raf){last=0;raf=requestAnimationFrame(tick);}}
  reduce.addEventListener('change',()=>{draw();sync();});document.addEventListener('visibilitychange',sync);
  if('IntersectionObserver' in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync();},{threshold:0}).observe(root);
  let resizeFrame=0;window.addEventListener('resize',()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(resize);});
  show(startIndex);resize();sync();
  }

  const menu=document.querySelector('.menu');
  function findHash(hash){try{return hash?document.getElementById(decodeURIComponent(hash.slice(1))):null;}catch{return null;}}
  function openHash(){const target=findHash(location.hash);if(target instanceof HTMLDetailsElement)target.open=true;return target;}
  document.addEventListener('click',event=>{
    const link=event.target.closest('a[href^="#"]');if(!link)return;const target=findHash(link.hash);if(!target)return;
    const fromMenu=menu?.contains(link);if(menu)menu.open=false;
    if(target instanceof HTMLDetailsElement){target.open=true;requestAnimationFrame(()=>{target.scrollIntoView({behavior:reduce.matches?'instant':'smooth',block:'start'});target.querySelector('summary').focus({preventScroll:true});});}
    else if(fromMenu){target.setAttribute('tabindex','-1');target.focus({preventScroll:true});}
  });
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&menu?.open){menu.open=false;menu.querySelector('summary').focus();}});
  matchMedia('(min-width:981px)').addEventListener('change',event=>{if(event.matches&&menu)menu.open=false;});
  function syncLanguageLinks(){document.querySelectorAll('.language-nav a').forEach(link=>{link.hash=location.hash;});}
  syncLanguageLinks();window.addEventListener('hashchange',()=>{openHash();syncLanguageLinks();});const target=openHash();if(target)requestAnimationFrame(()=>target.scrollIntoView({behavior:'instant',block:'start'}));
})();
