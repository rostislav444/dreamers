import React, { useState, useRef } from 'react';
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
import { CloseIcon, AddIcon, MinusIcon } from '@chakra-ui/icons';
import { TransformWrapper, TransformComponent } from 'react-zoom-pan-pinch';
import type { ReactZoomPanPinchRef } from 'react-zoom-pan-pinch';
import { CameraImage, CameraImagesWrapper } from './style';
import { MEDIA_URL } from '@/local';

interface ProductGalleryModalProps {
    isOpen: boolean;
    onClose: () => void;
    images: string[];
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
    const images = cameras[currentImageIndex].map(camera => camera.image);

    const [loaded, setLoaded] = useState<boolean[]>(new Array(images.length).fill(false));
    const transformRef = useRef<ReactZoomPanPinchRef | null>(null);
    const isMobile = useBreakpointValue({ base: true, md: false });

    const handleImageLoad = (index: number) => {
        const newLoaded = [...loaded];
        newLoaded[index] = true;
        setLoaded(newLoaded);
    };

    return (
        <Modal isOpen={isOpen} onClose={onClose} size="full">
            <ModalOverlay bg="white" />
            <ModalContent
                maxWidth={'100vw'}
                maxHeight={'100vh'}
                bg="transparent"
            >
                <ModalBody p={0} position="relative">
                    <TransformWrapper
                        ref={transformRef}
                        initialScale={1}
                        minScale={0.1}
                        maxScale={4}
                        centerOnInit
                        limitToBounds={false}
                        smooth
                    >
                        {({ zoomIn, zoomOut, resetTransform }) => (
                            <Box position="relative" height={"100vh"}>
                                {/* Кнопки управления */}
                                <Flex position="absolute" left={4} top={4} zIndex={2} gap={2}>
                                    <IconButton
                                        aria-label="Zoom in"
                                        icon={<AddIcon />}
                                        onClick={() => zoomIn()}
                                        colorScheme="whiteAlpha"
                                    />
                                    <IconButton
                                        aria-label="Zoom out"
                                        icon={<MinusIcon />}
                                        onClick={() => zoomOut()}
                                        colorScheme="whiteAlpha"
                                    />
                                    <IconButton
                                        aria-label="Reset"
                                        icon={<CloseIcon />}
                                        onClick={() => resetTransform()}
                                        colorScheme="whiteAlpha"
                                    />
                                </Flex>

                                {/* Кнопка закрытия */}
                                <IconButton
                                    aria-label="Close modal"
                                    icon={<CloseIcon />}
                                    position="absolute"
                                    right={4}
                                    top={4}
                                    zIndex={2}
                                    onClick={onClose}
                                    colorScheme="whiteAlpha"
                                />

                                {/* Основное содержимое */}
                                <TransformComponent
                                    wrapperStyle={{
                                        width: '100vw',
                                        height: '100vh',
                                    }}
                                >
                                    <Box
                                        width="1950px"
                                        height="1300px"
                                        position="relative"
                                    >
                                        {images.map((image, index) => (
                                            <img
                                                key={index}
                                                src={`/api/image-proxy?url=${encodeURIComponent(MEDIA_URL + image)}`}
                                                alt={`Product layer ${index + 1}`}
                                                style={{
                                                    position: 'absolute',
                                                    top: 0,
                                                    left: 0,
                                                    width: '100%',
                                                    height: '100%',
                                                    opacity: loaded[index] ? 1 : 0,
                                                    transition: 'opacity 0.3s'
                                                }}
                                                onLoad={() => handleImageLoad(index)}
                                            />
                                        ))}
                                    </Box>
                                </TransformComponent>

                                {/* Миниатюры */}
                                <Flex
                                    position="fixed"
                                    bottom="0"
                                    left={0}
                                    right={0}
                                    justifyContent="center"
                                    px={4}
                                    gap={2}
                                    overflow="auto"
                                    bg="blackAlpha.300"
                                    py={2}
                                    height="80px"
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
                                            _hover={{ borderColor: "brown.300" }}
                                            width={isMobile ? "60px" : "80px"}
                                            height={isMobile ? "40px" : "53px"}
                                            display="flex"
                                            alignItems="center"
                                        >
                                            <CameraImagesWrapper>
                                                {camera.map((image, imageKey) => (
                                                    <CameraImage
                                                        key={imageKey}
                                                        src={`/api/image-proxy?url=${encodeURIComponent(MEDIA_URL + image.thumbnails?.s)}`}
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
            </ModalContent>
        </Modal>
    );
};

export default ProductGalleryModal;