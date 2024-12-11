import {Box} from "@chakra-ui/react";
import {useState} from "react";
import {MEDIA_URL} from "@/local";
import {Model3dInterface, ProductInterface} from "@/interfaces/Product";
import {SelectedMaterialsInterface} from "@/interfaces/Materials";
import {CameraImageFromMaterials} from "@/utils/Product/Materials";
import ProductGalleryModal from "@/components/App/Product/Galery/components/PanZoom";
import ProductInterior from "@/components/App/Product/Galery/components/Interiors";
import MainGallery from "@/components/App/Product/Galery/components/MainGallery";
import Thumbnails from "@/components/App/Product/Galery/components/Thumbnails";


interface ProductGalleryProps {
    mobile: boolean;
    product: ProductInterface;
    selectedMaterials: SelectedMaterialsInterface;
}

const getCameraPartsImages = (models3d: Model3dInterface, selectedMaterials: SelectedMaterialsInterface) => {
    return models3d.cameras.map(camera => CameraImageFromMaterials(camera.parts, selectedMaterials));
};

export const ProductGallery = ({mobile, product, selectedMaterials}: ProductGalleryProps) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const cameras = product.model_3d.flatMap(model_3d => getCameraPartsImages(model_3d, selectedMaterials));
    const model3dCameras = product.model_3d.flatMap(model_3d => model_3d.cameras);
    const [currentImage, setCurrentImage] = useState<number>(cameras.length > 1 ? 1 : Math.round(cameras.length / 3));
    const currentCamera = model3dCameras[currentImage];
    const [selectedInterior, setSelectedInterior] = useState<any[]>(currentCamera.interior_layers.map(() => null));
    const [showInterior, setShowInterior] = useState<boolean>(true);

    const handleArrowClick = (direction: number) => {
        if (direction < 0) {
            setCurrentImage(cameras.length - 1);
        } else if (direction >= cameras.length) {
            setCurrentImage(0);
        } else {
            setCurrentImage(direction);
        }
    };

    const handleSelectedInterior = (key: number, materialKey: number | null) => {
        const newSelectedInterior = [...selectedInterior];
        newSelectedInterior[key] = materialKey;
        setSelectedInterior(newSelectedInterior);
    };

    const interiors = currentCamera.interior_layers
        .map((layer: any, i: number) => {
            if (selectedInterior[i] !== null) {
                return mobile
                    ? MEDIA_URL + layer.materials[selectedInterior[i]].image_thumbnails.m
                    : layer.materials[selectedInterior[i]].image;
            }
            return null;
        }).filter((interior) => interior !== null) as string[];

    const interiorsAlt = currentCamera.interior_layers
        .map((layer: any, i: number) => {
            if (selectedInterior[i] !== null) {
                return MEDIA_URL + layer.materials[selectedInterior[i]].image_thumbnails.s;
            }
            return null;
        }).filter((interior) => interior !== null) as string[];

    const images = [...interiors, ...cameras[currentImage].map(
        image => `${MEDIA_URL}${mobile ? image.thumbnails?.m : image.image}`)] as string[];
    const imagesAlt = [...interiorsAlt, ...cameras[currentImage].map(image => `${MEDIA_URL}${image.thumbnails?.s}`)];

    return (
        <>
            <Box w='100%'>
                <MainGallery images={images} imagesAlt={imagesAlt} currentImage={currentImage}
                             handleArrowClick={handleArrowClick} setIsModalOpen={setIsModalOpen}/>
                <Thumbnails mobile={mobile} cameras={cameras} currentImage={currentImage}
                            setCurrentImage={setCurrentImage}/>
                <ProductInterior mobile={mobile} currentCamera={currentCamera} selectedInterior={selectedInterior}
                                 showInterior={showInterior} setShowInterior={setShowInterior}
                                 handleSelectedInterior={handleSelectedInterior}/>
            </Box>
            <ProductGalleryModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}
                                 cameras={cameras} currentImageIndex={currentImage} onImageChange={setCurrentImage}/>
        </>
    );
};