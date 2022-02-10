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
            console.log('logged in and sending data ...')
        }

    })
}