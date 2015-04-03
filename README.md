#Dichotomous Language

The Dichotomous Language can be used to build up dichotomous keys that can be used to classify objects defined in a objects file.

Although referred to internally as rules by the interpreter, it is better to think of them as steps. Steps are separated by `%%` and control the flow through a dichotomous key.

```
step 1
%%
step 2
%%
; This is a comment
step 3
```

Each step contains two (or possibly more) conditions detailing program flow. They are setup as such:

```
condition_to_be_met:action:data
```

`condition_to_be_met` can be any string that does not have a colon, such as `has_compound_leaves`. The action is `goto` or `result` depending on the situation. Use `goto` when you want to go to another setup, in which case `data` the step number you want to go to, like 2 or 3. If the action is `result`, then `data` is the final  classification of the object.

If you want to specify that a condition should not be met, prefix it with an exclamation point.

```
; Object should not have compound leaves
!has_compound_leaves:goto:4
```

If you want to create a condition that is always met, use the special condition `*`. Since conditions are evaluated in order, put this at the end of the step, or any conditions after it will not be evaluated.

```
; This condition is always true
*:result:Homo sapiens
```

If you want to specify a result as indeterminate, i.e. no classification is possible, use the special result `indet`

```
has_eyes:goto:4
; If the object does not have eyes, we don't know what it is
!has_eyes:result:indet
```

By default, if no condition is true for an object in a step, the result `indet` is returned. This is the equivalent of putting the condition `*:result:indet` at the end of each step.

To see an example of a key file, look at `writing.dck`, which is a dichotomous key setup to classify different writing utensils.

Once you have your key file, you have to create a list of objects. This is similar in setup to the key file.

```
Object 1 Name
characteristic_of_object
; This is a comment
%%
Object 2 Name
characteristic_of_object
characteristic2_of_object
```

Each object must have a name, which is placed at the top of its definition. Object are separated by `%%`. Then, below the name, place all characteristics tested for that are met by the object, such as `has_compound_leaves`. If a characteristic is not placed in an object definition, it is assumed that the object does not have this characteristic. But, if you want to drive home the point, you can prefix the characteristic name with an exclamation point.

```
Object 1
; Does not have compound leaves
has_red_leaves
%%
Object 2
; Does not have compound leaves
!has_compound_leaves
```

To see an example of an objects file look at `writing.dco`, which goes along with `writing.dck`.

#Dichotomous Interpreter

To run the dichotomous interpreter, run

```
./dichotomous.py key_file.dck objects_file.dco
```

You may have to use another method to invoke the python script `dichotomous.py`, but the first argument is always the key file, and the second argument is always the objects file, such as `./dichotomous.py writing.dck writing.dco`

The interpreter will iterate through all of the objects and produce a list on standard output like

```
1. Object 1: Ink Pen
2. Object 2: Crayon
3. Object 3: Crayon
4. Object 4: Colored Pencil
5. Object 5: Sharpie
6. Object 6: Marker
```





