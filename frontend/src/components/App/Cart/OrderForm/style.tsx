import { Input, InputProps, Textarea, TextareaProps } from '@chakra-ui/react';
import React, { forwardRef } from "react";


const placeholderStyle = { fontSize: "14px", marginLeft: "6px", color: 'brown.500' }

export const CustomInput = forwardRef<HTMLInputElement, InputProps>((props, ref) => (
  <Input
    _placeholder={placeholderStyle}
    _focus={{ boxShadow: "none", "&:focus": { outline: "none" } }}
    ref={ref}
    {...props}
  />
));

CustomInput.displayName = "CustomInput";

export const CustomTextarea = forwardRef<HTMLTextAreaElement, TextareaProps>((props, ref) => (
  <Textarea
    _placeholder={{...placeholderStyle, paddingTop: '2px'}}
    _focus={{ boxShadow: "none", "&:focus": { outline: "none" } }}
     ref={ref}
    {...props}
  />
));


CustomTextarea.displayName = "CustomTextarea";
