#lang racket
(require racket/draw
         racket/gui/easy
         racket/gui/easy/operator)

(define gzdoom-run "/usr/bin/gzdoom-run")
(define gzdoom-icon "/usr/share/icons/gzdoom.png")
(define version-major 1)
(define version-minor 3)
(define version-patch 1)


(define (close-ports in out err)
    (close-input-port out)
    (close-output-port in)
    (close-input-port err))


(define (make-system-font size)
  (make-object font% size 'system))

(define (string-join/lines v)
  (string-join v "\n"))

(define (string-replace/modulo v)
  (string-replace v " " "%"))

(define/obs @wad-list 
  (let-values ([(sp out in err) (subprocess #f #f #f gzdoom-run "list")])
    (let loop ()
      (when (eq? (subprocess-status sp) 'running)
        (loop)))
    (let ([wad-list (port->string out)])
      (close-ports in out err)
      (string-split wad-list "\n"))))

(define/obs @run-args (car (obs-peek @wad-list)))

(define/obs @mod-list 
  (vpanel
   #:style '(vscroll border)
   (text
    #:font (make-system-font 13.5)
    (@wad-list . obs-map . string-join/lines))))


(define (launch-gzdoom) 
  (let-values ([(proc out in err) (subprocess #f #f #f gzdoom-run "with" (string-replace (obs-peek @run-args) " " "%"))])
    (let loop ()
      (when (eq? (subprocess-status proc) 'running)
        (loop)))
    (if (= (subprocess-status proc) 0)
        (close-ports in out err)
        (let ([message (port->string out)])
          (close-ports in out err)
          (error message)))))


(define/obs @render-window
  (window
   #:title (format "GZDoom Run v~a.~a.~a" 
                   version-major 
                   version-minor
                   version-patch)
   #:size '(500 500)
   (image gzdoom-icon)
   (vpanel
    #:style '(border)
    (text "Mod List" #:font (make-system-font 18.0))
    (obs-peek @mod-list)
    (hpanel
     #:stretch '(#t #f) 
     (input 
      #:label " Launch With"
      #:stretch '(#t #f)
      #:min-size '(400 #f)
      (@run-args . obs-map . values)
      (lambda (e v) (obs-set! @run-args v)))))
   (hpanel
    #:alignment '(right center)
    #:stretch '(#t #f)
    (button "Run" launch-gzdoom)
    (button "Clear" (lambda () (obs-set! @run-args "")))
    (button "Exit" (lambda () (exit))))))

(render (obs-peek @render-window))