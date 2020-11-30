const busca=document.querySelector("#busca")

busca.addEventListener('Keyup', (e)=>{
  const buscaValor=e.target.value;

  if(buscaValor.length>0):
    console.log('buscaValor: ', buscaValor)

})
