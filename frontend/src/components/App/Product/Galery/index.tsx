import {Model3dInterface, ProductInterface} from "@/interfaces/Product";
import {
    CameraImage,
    CameraImagesWrapper,
    GalleryArrowWrapper,
    MainImageWrapper
} from "@/components/App/Product/Galery/style";
import {Box, Flex, Grid, GridItem, Heading, IconButton} from "@chakra-ui/react";
import Image from 'next/image'
import {BASE_URL, MEDIA_URL} from "@/local";
import {useEffect, useState} from "react";
import {CameraImageFromMaterials} from "@/utils/Product/Materials";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {ChevronUpIcon, DownloadIcon} from "@chakra-ui/icons";
import {handleImageMergeAndDownload} from "@/components/App/Product/Galery/utils";

interface ProductGalleryProps {
    mobile: boolean
    product: ProductInterface,
    selectedMaterials: SelectedMaterialsInterface
}

const getCameraPartsImages = (models3d: Model3dInterface, selectedMaterials: SelectedMaterialsInterface) => {
    return models3d.cameras.map(camera => CameraImageFromMaterials(camera.parts, selectedMaterials))
}

const LazyImage = ({lowResSrc, highResSrc, alt, index, totalLayers}: {
    lowResSrc: string,
    highResSrc: string,
    alt: string,
    index: number,
    totalLayers: number
}) => {
    const [src, setSrc] = useState<string>(lowResSrc);
    const [isLoaded, setIsLoaded] = useState<boolean>(false);

    useEffect(() => {
        setSrc(lowResSrc);
        setIsLoaded(false);
    }, [lowResSrc, highResSrc]);

    const handleImageLoad = () => {
        setIsLoaded(true);
        setSrc(highResSrc);
    };

    const getLayerStyles = () => {
        const baseStyles = {
            transition: 'all 0.5s',
            opacity: isLoaded ? 1 : 0.2,
            filter: isLoaded ? 'blur(0)' : 'blur(10px)',
            objectFit: 'contain' as const,
        };

        // Внутренние слои
        if (index > 0 && index < totalLayers - 1) {
            return {
                ...baseStyles,
                imageRendering: 'pixelated' as const,
            };
        }

        // Верхний слой (контур)
        if (index === totalLayers - 1) {
            return {
                ...baseStyles,
                imageRendering: 'auto' as const,
                WebkitMaskImage: 'radial-gradient(circle at center, black 98%, transparent 100%)',
                maskImage: 'radial-gradient(circle at center, black 98%, transparent 100%)',
            };
        }

        // Нижний слой
        return baseStyles;
    };

    return (
        <Image
            unoptimized={true}
            src={src}
            alt={alt}
            fill={true}
            loading='lazy'
            onLoadingComplete={handleImageLoad}
            style={getLayerStyles()}
        />
    );
};

export const ProductGallery = ({mobile, product, selectedMaterials}: ProductGalleryProps) => {
    const cameras = product.model_3d.flatMap(model_3d => getCameraPartsImages(model_3d, selectedMaterials));
    const model3dCameras = product.model_3d.flatMap(model_3d => model_3d.cameras);
    const [currentImage, setCurrentImage] = useState<number>(Math.round(cameras.length / 3));
    const currentCamera = model3dCameras[currentImage];
    const [selectedInterior, setSelectedInterior] = useState<any[]>(currentCamera.interior_layers.map(() => null));
    const [showInterior, setShowInterior] = useState<boolean>(true);
    const hasInterior = currentCamera.interior_layers.length > 0;

    const handleContextMenuOpen = (e: any) => {
        if (e.target.tagName.toLowerCase() === 'img') {
            e.preventDefault();
        }
    };

    const handleArrowClick = (direction: number) => {
        if (direction < 0) {
            setCurrentImage(cameras.length - 1);
        } else if (direction >= cameras.length) {
            setCurrentImage(0);
        } else {
            setCurrentImage(direction);
        }
    };

    const interiors = currentCamera.interior_layers
        .map((layer, i) => {
            if (selectedInterior[i] !== null) {
                return mobile
                    ? MEDIA_URL + layer.materials[selectedInterior[i]].image_thumbnails.m
                    : layer.materials[selectedInterior[i]].image;
            }
            return null;
        }).filter((interior) => interior !== null) as string[];

    const interiorsAlt = currentCamera.interior_layers
        .map((layer, i) => {
            if (selectedInterior[i] !== null) {
                return MEDIA_URL + layer.materials[selectedInterior[i]].image_thumbnails.s;
            }
            return null;
        }).filter((interior) => interior !== null) as string[];

    const images = [...interiors, ...cameras[currentImage].map(
        image => `${MEDIA_URL}${mobile ? image.thumbnails?.m : image.image}`)] as string[];
    const imagesAlt = [...interiorsAlt, ...cameras[currentImage].map(
        image => `${MEDIA_URL}${image.thumbnails?.s}`)] as string[];

    const handleSelectedInterior = (key: number, materialKey: number | null) => {
        const newSelectedInterior = [...selectedInterior];
        newSelectedInterior[key] = materialKey;
        setSelectedInterior(newSelectedInterior);
    };

    return (
        <Box w='100%'>
            <MainImageWrapper>
                {images.reverse().map((image: string, imageKey: number) =>
                    <LazyImage
                        key={imageKey}
                        lowResSrc={imagesAlt[imageKey]}
                        highResSrc={image}
                        alt='img'
                        index={imageKey}
                        totalLayers={images.length}
                    />
                )}
                <GalleryArrowWrapper
                    left={true}
                    onClick={() => handleArrowClick(currentImage - 1)}>
                    {'<'}
                </GalleryArrowWrapper>
                <GalleryArrowWrapper
                    left={false}
                    onClick={() => handleArrowClick(currentImage + 1)}>
                    {'>'}
                </GalleryArrowWrapper>
                <IconButton
                    aria-label='download'
                    icon={<DownloadIcon color='brown.500'/>}
                    position='absolute'
                    top='4'
                    right='4'
                    onClick={() => handleImageMergeAndDownload(images)}
                    variant='ghost'
                />
            </MainImageWrapper>

            <Grid
                mt={2}
                mb={4}
                mr={mobile ? 0 : 20}
                w={mobile ? '100%' : '80%'}
                gridTemplateColumns={
                    mobile
                        ? 'repeat(auto-fill, minmax(60px, 1fr))'
                        : 'repeat(auto-fill, minmax(80px, 1fr))'
                }
                gap={2}
            >
                {cameras.map((camera, key) =>
                    <GridItem
                        key={key}
                        onClick={() => setCurrentImage(key)}
                        border={currentImage === key ? '2px solid brown' : '2px solid #fff'}
                        _hover={{
                            borderColor: 'beige',
                        }}
                        cursor='pointer'
                    >
                        <CameraImagesWrapper onContextMenu={handleContextMenuOpen}>
                            {camera.map((image, imageKey) => (
                                <CameraImage
                                    className='camera-image'
                                    key={imageKey}
                                    src={MEDIA_URL + image.thumbnails?.m}
                                />
                            ))}
                        </CameraImagesWrapper>
                    </GridItem>
                )}
            </Grid>

            {hasInterior && (
                <Box>
                    <Flex
                        justifyContent='space-between'
                        alignItems='center'
                        onClick={() => setShowInterior(!showInterior)}
                    >
                        <Heading size='md'>Інтер&apos;ер</Heading>
                        <ChevronUpIcon
                            w='6'
                            h='6'
                            color='brown.500'
                            cursor='pointer'
                            transform={showInterior ? 'rotate(180deg)' : 'rotate(0deg)'}
                        />
                    </Flex>
                    {showInterior && (
                        <Box mt='4'>
                            {model3dCameras[currentImage].interior_layers.map((layer, key) => (
                                <Grid
                                    gridTemplateColumns={
                                        mobile
                                            ? 'repeat(auto-fill, minmax(60px, 1fr))'
                                            : 'repeat(auto-fill, minmax(100px, 1fr))'
                                    }
                                    gap={2}
                                    mb='2'
                                    key={key}
                                >
                                    <Box
                                        borderWidth='2px'
                                        borderColor={selectedInterior[key] === null ? 'brown.500' : 'white'}
                                        onClick={() => handleSelectedInterior(key, null)}
                                    />
                                    {layer.materials.map((material, materialKey) => (
                                        <Box
                                            pos='relative'
                                            borderWidth='2px'
                                            key={materialKey}
                                            pt='66%'
                                            borderColor={selectedInterior[key] === materialKey ? 'brown.500' : 'white'}
                                        >
                                            <Image
                                                fill={true}
                                                onClick={() => handleSelectedInterior(key, materialKey)}
                                                quality={100}
                                                src={MEDIA_URL + material.image_thumbnails?.s}
                                                alt='img'
                                            />
                                        </Box>
                                    ))}
                                </Grid>
                            ))}
                        </Box>
                    )}
                </Box>
            )}
        </Box>
    );
};