import React from 'react';
import {ChevronLeftIcon, ChevronRightIcon} from '@chakra-ui/icons'

interface ChevronIconProps {
  onClick: () => void;
}

export const ChevronLeft: React.FC<ChevronIconProps> = ({ onClick }) => (
  <ChevronLeftIcon
    onClick={onClick}
    position='absolute'
    w={12}
    h={12}
    left={0}
    top='calc(50% - 24px)'
    cursor='pointer'
    zIndex={1000}
  />
);


export const ChevronRight: React.FC<ChevronIconProps> = ({ onClick }) => (
  <ChevronRightIcon
    onClick={onClick}
    position='absolute'
    w={12}
    h={12}
    right={0}
    top='calc(50% - 24px)'
    cursor='pointer'
    zIndex={1000}
  />
);
