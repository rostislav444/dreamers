import React from 'react';
import {ChevronLeftIcon, ChevronRightIcon} from '@chakra-ui/icons'

interface ChevronIconProps {
  onClick: () => void;
  mobile: boolean
}

export const ChevronLeft: React.FC<ChevronIconProps> = ({ onClick, mobile }) => (
  <ChevronLeftIcon
    onClick={onClick}
    position='absolute'
    w={mobile ? 8 : 12}
    h={mobile ? 8 : 12}
    left={mobile ? '-8px' : 0}
    top='calc(50% - 24px)'
    cursor='pointer'
    zIndex={1000}
  />
);


export const ChevronRight: React.FC<ChevronIconProps> = ({ onClick, mobile }) => (
  <ChevronRightIcon
    onClick={onClick}
    position='absolute'
    w={mobile ? 8 : 12}
    h={mobile ? 8 : 12}
    right={mobile ? '-8px' : 0}
    top='calc(50% - 24px)'
    cursor='pointer'
    zIndex={1000}
  />
);
