using StaticArrays: SVector, MVector

export Particle
export distance, potential_energy, acceleration, accelerationof, distribute!, initialize!

const ε = 120
const σ = 0.34
const ρ = 0.75

mutable struct Particle
    r::MVector{3,Float64}
    v::MVector{3,Float64}
    Particle() = new()  # Incomplete initialization
end

function distance(particle::Particle, particle′::Particle)
    return sqrt(sum(abs2, particle.r - particle′.r))
end

function potential_energy(particle::Particle, particle′::Particle)
    r = distance(particle, particle′)
    η = 1 / r^6
    return 4ε * η * (η - 1)
end
function potential_energy(particles)
    total = 0
    for (i, particleᵢ) in enumerate(particles)
        for particleⱼ in particles[i:end]
            total += potential_energy(particleᵢ, particleⱼ)
        end
    end
    return 2total
end

function acceleration(particle::Particle)
    return function (particle′::Particle)
        η = 1 / distance(particle, particle′)
        return (particle.r - particle′.r) * (η^14 - η^8)
    end
end

function accelerationof(particles, i)
    return sum(filter(!=(i), eachindex(particles))) do j
        acceleration(particles[i])(particles[j])
    end
end
accelerationof(particles) = map(Base.Fix1(accelerationof, particles), eachindex(particles))

function distribute!(particles, volume)
    n = length(particles)
    @assert n > 0
    a = cbrt(volume)
    for (particle, coordinates) in zip(particles, eachcol(a * rand(3, n)))
        particle.r = coordinates
    end
    @assert unique(particles) == particles
    return particles
end

function initialize!(particles)
    @assert length(particles) > 0
    for particle in particles
        particle.v = zeros(MVector{3,Float64})
    end
    return particles
end
