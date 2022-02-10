var updateBts = document.getElementsByClassName('add-cart-btn')


for(var i = 0; i < updateBts.length; i++){
    updateBts[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action  = this.dataset.action
        console.log('productId:', productId, 'action:',action)

        console.log('USER:', user)
        if (user === 'AnonymousUser'){
            console.log('not logged in')
        }else{
            updateUserOrder(productId, action)
        }

    })
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data ...')

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'productId:',productId, 'action:', action})
    })

}