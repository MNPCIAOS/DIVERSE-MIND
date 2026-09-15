(() => {
  const themes = [
    ['Library Gold',42,'#c99518'],['Oak & Paper',32,'#9a6a2f'],['Forest Canopy',118,'#2f6b45'],['Moss Garden',92,'#687d3c'],['Sage Leaf',78,'#6c8b70'],
    ['Pine Study',150,'#35634f'],['Cedar Grove',28,'#9a6844'],['Olive Branch',72,'#77843b'],['Bamboo Ink',112,'#5d8b62'],['Tea House',34,'#a77842'],
    ['Coffee & Books',24,'#7d5135'],['Warm Walnut',26,'#805634'],['Mahogany Library',8,'#7c3027'],['Cocoa Pages',18,'#82563d'],['Sandstone',38,'#ad8352'],
    ['Desert Sage',58,'#8a8b63'],['Dried Herb',48,'#9b7952'],['Terracotta',20,'#b65e3d'],['Clay Pot',15,'#a95b48'],['Rosewood',350,'#7e3542'],
    ['Autumn Leaves',34,'#a66a2e'],['Maple Study',25,'#b26a35'],['Amber Paper',45,'#b58a29'],['Honey Book',50,'#c08a21'],['Sunlit Desk',48,'#c69a3b'],
    ['Linen & Ink',205,'#667b8a'],['Parchment',45,'#b59c76'],['Ivory Shelf',48,'#a99572'],['Cream Paper',42,'#c2a76c'],['Vintage Sepia',35,'#886b4b'],
    ['Midnight Library',220,'#6c7dba'],['Deep Forest',145,'#4c7b63'],['Evergreen Night',150,'#3c7560'],['Blue Ink',210,'#4f729c'],['Navy Scholar',215,'#526b96'],
    ['Rainy Window',200,'#6f8fa1'],['Plum Study',285,'#86638e'],['Berry Bookshop',320,'#9a4d69'],['Burgundy Leather',350,'#873b45'],['Copper Bookmark',28,'#b66b39'],
    ['Bronze Classics',30,'#9b713d'],['Golden Hour',43,'#c68b2d'],['Meadow Reader',105,'#65905b'],['Wildflower',330,'#9b678e'],['Lavender Herb',270,'#8576a8'],
    ['Eucalyptus',155,'#5d8b80'],['Mint Paper',165,'#62a18c'],['River Stone',195,'#71848b'],['Mountain Cabin',25,'#7a5d46'],['Coastal Reading',200,'#54879a']
  ];
  const picker=document.querySelector('#theme-picker'), mode=document.querySelector('#mode-toggle');
  themes.forEach(([name],i)=>{const o=document.createElement('option');o.value=i;o.textContent=name+' Theme';picker?.appendChild(o)});
  const state={theme:Number(localStorage.getItem('dm-theme-index')||0),night:localStorage.getItem('dm-night')==='1'};
  function apply(){
    const [name,h,accent]=themes[state.theme]||themes[0], r=document.documentElement;
    r.style.setProperty('--accent',accent); r.style.setProperty('--accent-soft',`hsl(${h} 42% 88%)`);
    if(state.night){r.style.setProperty('--bg',`hsl(${h} 18% 8%)`);r.style.setProperty('--panel',`hsl(${h} 16% 13%)`);r.style.setProperty('--panel2',`hsl(${h} 15% 18%)`);r.style.setProperty('--text','#f4f1e8');r.style.setProperty('--muted','#b7b09f');r.style.setProperty('--line',`hsl(${h} 12% 28%)`);r.style.setProperty('--deep',`hsl(${h} 22% 5%)`)}
    else{r.style.setProperty('--bg',`hsl(${h} 24% 96%)`);r.style.setProperty('--panel','#fffdf8');r.style.setProperty('--panel2',`hsl(${h} 22% 91%)`);r.style.setProperty('--text',`hsl(${h} 25% 13%)`);r.style.setProperty('--muted',`hsl(${h} 12% 42%)`);r.style.setProperty('--line',`hsl(${h} 18% 83%)`);r.style.setProperty('--deep',`hsl(${h} 25% 11%)`)}
    document.documentElement.dataset.night=state.night?'true':'false'; if(picker)picker.value=String(state.theme); if(mode)mode.textContent=state.night?'☀️ Day mode':'🌙 Night mode';
    localStorage.setItem('dm-theme-index',String(state.theme));localStorage.setItem('dm-night',state.night?'1':'0');
  }
  picker?.addEventListener('change',()=>{state.theme=Number(picker.value);apply()}); mode?.addEventListener('click',()=>{state.night=!state.night;apply()}); apply();
})();
