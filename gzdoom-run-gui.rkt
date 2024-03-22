#! /usr/bin/racket
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

(define/obs @run-args "")


(define/obs @wad-list 
  (let-values ([(sp out in err) (subprocess #f #f #f gzdoom-run "list")])
    (let loop ()
      (when (eq? (subprocess-status sp) 'running)
        (loop)))
    (let ([wad-list (port->string out)])
      (close-ports in out err)
      wad-list)))


(define/obs @mod-list 
  (vpanel
   #:style '(vscroll border)
   (text (obs-peek @wad-list) #:font (make-object font% 13.5 'system))))


(define (launch-gzdoom) 
  (let-values ([(proc out in err) (subprocess #f #f #f gzdoom-run (obs-peek @run-args))])
    (let loop ()
      (when (eq? (subprocess-status proc) 'running)
        (loop)))
    (if (= (subprocess-status proc) 0)
        (close-ports in out err)
        (let ([message (port->string err)])
          (close-ports in out err)
          (error message)))))


(define/obs @render-window
  (window
   #:title (format "GZDoom Run v~a.~a.~a" 
                   version-major 
                   version-minor
                   version-patch)
   #:size '(300 500)
   (image gzdoom-icon)
   (vpanel
    #:style '(border)
    (text "Mod List" #:font (make-object font% 18.0 'system))
    (obs-peek @mod-list)
    (hpanel
     #:stretch '(#t #f) 
     (input 
      #:label " Launch With"
      #:stretch '(#t #f)
      #:min-size '(400 #f)
      (obs-peek @run-args)
      (lambda (e v) (obs-set! @run-args v)))
     (button "Clear" (lambda () (obs-set! @run-args "")))))
   (hpanel
    #:stretch '(#t #f) 
    (button "Exit" (lambda () (exit))) 
    (button "Launch" launch-gzdoom))))

(render (obs-peek @render-window))