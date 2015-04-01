# UIComponentDescriptor2XML
this script is use to convert UIComponentDescriptor to xml file

warrning: it has many bugs =_=

When decompile a Flex project, you may found it difficult to read some .as files. 
that's because decompiler doesn't decompile it completely to MXML file, which may be like this:

```ActionScript
new UIComponentDescriptor({
    "type":Canvas,
    "id":"mainCanvas",
    "stylesFactory":function ():void {
        this.borderStyle = "none";
        color = 0xFFFFFF;
    },
    "propertiesFactory":function ():Object {
        return ({
            "label":"main",
            "percentWidth":100,
            "percentHeight":100,
            "visible":true,
            "childDescriptors":[
                new UIComponentDescriptor({
                    "type":CheckBox,
                    "id":"check",
                    "events":{"click":"__check_click"},
                    "stylesFactory":function ():void {
                        this.fontSize = 12;
                    },
                    "propertiesFactory":function ():Object {
                        return ({
                            "x":39,
                            "y":8,
                            "label":"check",
                            "selected":false
                        });
                    }
                })
            ]
        });
    }
});
```

use this script, it can be convert to :

```XML
<?xml version="1.0" ?>
<mx:Canvas borderStyle="none" color="0xFFFFFF" id="mainCanvas" label="main" percentHeight="100" percentWidth="100" visible="true">
    <mx:CheckBox click="__check_click(event)" fontSize="12" id="check" label="check" selected="false" x="39" y="8"/>
</mx:Canvas>
```

use config file to setup, it can be written like this:

```
#this is the config file, lines that begin with '#' will be treated as comments
#write original file path and target file path like these examples
#@<D:\\a.as><D:\\b.xml>
#@<./a.as><C:\\b.xml>
#or you can ignore target path, if you do that, it will create a file in the same dir of original file
#@<D:\\a.as>
#and the target file will be D:\\a.as.xml

@<D:\\a.as>
@<D:\\c.as> <D:\\ccc.xml>

#to configure prefix of xml tags, you can write like this
#$<canvas><s:>
#it means each <canvas /> tag will become <s:canvas />

$<MyCanvas><UI:>

#to configure default prefix of other xml tags, you can write like this
#&<mx:>
#it means each tag that doesn't have matching prefix will use this as prefix, like : <mx:Label />

&<mx:>
```
