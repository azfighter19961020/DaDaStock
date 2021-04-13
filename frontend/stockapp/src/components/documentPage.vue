<template src="@/assets/documentation/template.html"></template>
<style scoped src="@/assets/css/googlecss.css"></style>
<style scoped src="@/assets/css/style.css"></style>
<script>
  export default({
    name:"documentPage",
    data(){
      return {
        login:false,
        elements:[]
      }
    },
    mounted(){
      this.calculElements()
      window.addEventListener('resize',this.calculElements())
      window.addEventListener('scroll', this.onScrollHandler)
    },
    destroyed () {
      window.removeEventListener('scroll', this.onScrollHandler)
    },
    methods:{
      calculElements(){
        var total_height = 0
        var eachelement = document.getElementsByClassName("content-section")
        var the_section = null
        for(var i=0;i<eachelement.length;i++){
          the_section = {}
          the_section.id = eachelement[i].getAttribute('id').replace('content-','')
          total_height += eachelement[i].offsetHeight
          the_section.max_height = total_height
          this.elements.push(the_section)
        }
      },
      scrollToCharacter(event){
        console.log("into onclick") 
        var id = event.currentTarget.getAttribute('data-target')
        document.getElementById(id).scrollIntoView({ behavior: 'smooth', block: 'center' })
        var elements = document.getElementsByClassName("scroll-to-link")
        var currentelement = event.currentTarget.parentElement
        for(var i=0;i<elements.length;i++){
          if(elements[i]!=currentelement){
            console.log("into if")
            elements[i].className = "scroll-to-link"
          }
          else{
            elements[i].className = "scroll-to-link active"
          }
        }
      },
      onScrollHandler(){
        let scrollHeight = window.pageYOffset
        var the_section = null
        var listelement = null
        var targetElement = null
        for(var i=0;i<this.elements.length;i++){
          the_section = this.elements[i]
          if(scrollHeight <= the_section.max_height){
            listelement = document.getElementsByClassName("scroll-to-link")
            targetElement = document.getElementsByClassName("scrolla")
            for(var j=0;j<listelement.length;j++){
              if(targetElement[j].getAttribute("data-target") == the_section.id){
                listelement[j].className = "scroll-to-link active"
              }
              else{
                listelement[j].className = "scroll-to-link"
              }
            }
            break
          }
        }
        if(scrollHeight + window.innerHeight > document.body.scrollHeight){
          listelement = document.getElementsByClassName("scroll-to-link")
          targetElement = document.getElementsByClassName("scrolla")
          for(j=0;j<listelement.length;j++){
            if(targetElement[j].getAttribute("data-target") == "Additional"){
              listelement[j].className = "scroll-to-link active"
            }
            else{
              listelement[j].className = "scroll-to-link"
            }
          }
        }
      }
    }
  })
</script>