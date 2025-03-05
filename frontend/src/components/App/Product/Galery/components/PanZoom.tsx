import React, {useRef, useEffect, useState} from 'react';
import {
    Modal,
    ModalOverlay,
    ModalContent,
    ModalBody,
    Box,
    Flex,
    IconButton,
    useBreakpointValue,
} from '@chakra-ui/react';
import {CloseIcon, AddIcon, MinusIcon} from '@chakra-ui/icons';
import {TransformWrapper, TransformComponent} from 'react-zoom-pan-pinch';
import type {ReactZoomPanPinchRef} from 'react-zoom-pan-pinch';
import {CameraImage, CameraImagesWrapper} from '../style';
import {MEDIA_URL} from '@/local';
import {LazyImage} from './LazyImage';

interface ProductGalleryModalProps {
    isOpen: boolean;
    onClose: () => void;
    cameras: Array<Array<{
        thumbnails?: {
            s: string;
            m: string;
        };
        image: string;
    }>>;
    currentImageIndex: number;
    onImageChange: (index: number) => void;
}

const ProductGalleryModal = ({
    isOpen,
    onClose,
    cameras,
    currentImageIndex,
    onImageChange
}: ProductGalleryModalProps) => {
    const transformRef = useRef<ReactZoomPanPinchRef | null>(null);
    const isMobile = useBreakpointValue({base: true, md: false});
    const [scale, setScale] = useState(1);

    const calculateInitialScale = () => {
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight; // Теперь используем полную высоту
        const imageWidth = 1950;
        const imageHeight = 1300;

        const scaleX = (viewportWidth * 0.9) / imageWidth;
        const scaleY = (viewportHeight * 0.9) / imageHeight;

        return Math.min(scaleX, scaleY);
    };

    const updateScale = () => {
        const newScale = calculateInitialScale();
        setScale(newScale);
        setTimeout(() => {
            if (transformRef.current) {
                transformRef.current.resetTransform();
                const viewportWidth = window.innerWidth;
                const viewportHeight = window.innerHeight;
                const imageWidth = 1950 * newScale;
                const imageHeight = 1300 * newScale;
                const x = (viewportWidth - imageWidth) / 2;
                const y = (viewportHeight - imageHeight) / 2;
                transformRef.current.setTransform(x, y, newScale);
            }
        }, 50);
    };

    useEffect(() => {
        if (isOpen) {
            updateScale();
            window.addEventListener('resize', updateScale);
            return () => window.removeEventListener('resize', updateScale);
        }
    }, [isOpen, updateScale]);

    useEffect(() => {
        if (isOpen) {
            updateScale();
        }
    }, [currentImageIndex, isOpen, updateScale]);

    const handleReset = () => {
        updateScale();
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} size="full">
            <ModalOverlay bg="white"/>
            <ModalContent maxWidth={'100vw'} maxHeight={'100vh'} bg="transparent">
                {isOpen && (
                    <ModalBody p={0} position="relative" overflow="hidden">
                        <TransformWrapper
                            ref={transformRef}
                            initialScale={scale}
                            minScale={scale * 0.5}
                            maxScale={4}
                            limitToBounds={false}
                            wheel={{step: 0.2}}
                            pinch={{step: 5}}
                            doubleClick={{mode: "reset"}}
                            onInit={() => {
                                updateScale();
                            }}
                        >
                            {({zoomIn, zoomOut}) => (
                                <Box position="relative" height="100vh">
                                    {/* Кнопки управления */}
                                    <Flex position="absolute" left={4} top={4} zIndex={2} gap={2}>
                                        <IconButton
                                            aria-label="Zoom in"
                                            icon={<AddIcon/>}
                                            onClick={() => zoomIn(0.2)}
                                            colorScheme="whiteAlpha"
                                        />
                                        <IconButton
                                            aria-label="Zoom out"
                                            icon={<MinusIcon/>}
                                            onClick={() => zoomOut(0.2)}
                                            colorScheme="whiteAlpha"
                                        />
                                        <IconButton
                                            aria-label="Reset"
                                            icon={<CloseIcon/>}
                                            onClick={handleReset}
                                            colorScheme="whiteAlpha"
                                        />
                                    </Flex>

                                    {/* Кнопка закрытия */}
                                    <IconButton
                                        aria-label="Close modal"
                                        icon={<CloseIcon/>}
                                        position="absolute"
                                        right={4}
                                        top={4}
                                        zIndex={2}
                                        onClick={onClose}
                                        colorScheme="whiteAlpha"
                                    />

                                    <TransformComponent
                                        wrapperStyle={{
                                            width: '100%',
                                            height: '100%',
                                        }}
                                    >
                                        <div style={{
                                            width: '1950px',
                                            height: '1300px',
                                        }}>
                                            {cameras[currentImageIndex].map((camera, index) => (
                                                <Box
                                                    key={index}
                                                    position="absolute"
                                                    top={0}
                                                    left={0}
                                                    width="100%"
                                                    height="100%"
                                                >
                                                    <LazyImage
                                                        lowResSrc={MEDIA_URL + camera.thumbnails?.m}
                                                        highResSrc={MEDIA_URL + camera.image}
                                                        alt={`Product layer ${index + 1}`}
                                                    />
                                                </Box>
                                            ))}
                                        </div>
                                    </TransformComponent>

                                    {/* Миниатюры теперь поверх изображения */}
                                    <Flex
                                        position="absolute"
                                        bottom={4}
                                        left="50%"
                                        transform="translateX(-50%)"
                                        justifyContent="center"
                                        px={4}
                                        gap={2}
                                        zIndex={2}
                                        bg="blackAlpha.300"
                                        py={2}
                                        borderRadius="md"
                                        maxWidth="100%"
                                        overflow="auto"
                                    >
                                        {cameras.map((camera, key) => (
                                            <Box
                                                key={key}
                                                onClick={() => onImageChange(key)}
                                                cursor="pointer"
                                                borderWidth={2}
                                                borderColor={currentImageIndex === key ? "brown.500" : "transparent"}
                                                borderRadius="md"
                                                overflow="hidden"
                                                flexShrink={0}
                                                transition="all 0.2s"
                                                _hover={{borderColor: "brown.300"}}
                                                width={isMobile ? "60px" : "80px"}
                                                height={isMobile ? "40px" : "53px"}
                                                display="flex"
                                                alignItems="center"
                                            >
                                                <CameraImagesWrapper>
                                                    {camera.map((image, imageKey) => (
                                                        <CameraImage
                                                            key={imageKey}
                                                            loading="lazy"
                                                            src={MEDIA_URL + image.thumbnails?.s}
                                                            alt={`Camera view ${key}`}
                                                        />
                                                    ))}
                                                </CameraImagesWrapper>
                                            </Box>
                                        ))}
                                    </Flex>
                                </Box>
                            )}
                        </TransformWrapper>
                    </ModalBody>
                )}
            </ModalContent>
        </Modal>
    );
};

export default ProductGalleryModal;