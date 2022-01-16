/**
 * @description Ripple 이펙트 영역을 생성하고 추가합니다.
 * @param {MouseEvent} e 마우스 이벤트 객체
 */
 function addRippleEffact (e) {
    const $this = this
    const size = Math.max(this.offsetWidth, this.offsetHeight)
    const x = e.offsetX
    const y = e.offsetY
    const ripple = createRippleElement(x, y, size)
    ripple.addEventListener('animationend', function () {
      $this.removeChild(this)
    })
    this.appendChild(ripple)
  }
  
  /**
   * @description 지정한 위치와 크기로 Ripple 이펙트 Element를 생성합니다.
   * @param {number} x 마우스 클릭 X
   * @param {number} y 마우스 클릭 Y
   * @param {number} size Ripple 이펙트 크기
   * @return {HTMLElement} Ripple 이펙트 Element
   */
  function createRippleElement (x, y, size) {
    const div = document.createElement('div')
    div.classList.add('ripple')
    div.style.left = x - size / 2 + 'px'
    div.style.top = y - size / 2 + 'px'
    div.style.width = div.style.height = size + 'px'
    return div
  }
  
  // 전역 객체에 $material 등록
  window.$material = {
    button: function (el) {
      el.onmousedown = addRippleEffact
    }
  }
  
  document.addEventListener('DOMContentLoaded', function () {
  
    const el_1 = document.getElementById('btn-1')
    const el_2 = document.getElementById('btn-2')
  
    $material.button(el_1)
    $material.button(el_2)
  
  })