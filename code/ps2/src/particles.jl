using StaticArrays: SVector, MVector

export Particle
export distance,
    potential_energy,
    kinetic_energy,
    total_energy,
    acceleration,
    accelerationof,
    rescale_velocities!,
    reset_velocities!,
    reset_positions!,
    reset!

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
    return 4η * (η - 1)
end
function potential_energy(particles)
    total = 0
    for (i, particleᵢ) in enumerate(particles[begin:(end - 1)])
        for particleⱼ in particles[(i + 1):end]
            total += potential_energy(particleᵢ, particleⱼ)
        end
    end
    return total
end

kinetic_energy(particle::Particle) = 24 * sum(abs2, particle.v)
kinetic_energy(particles) = sum(kinetic_energy, particles)

total_energy(particles) = kinetic_energy(particles) + potential_energy(particles)

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

function rescale_velocities!(particles, f)
    for particle in particles
        particle.v *= f
    end
    return particles
end

function reset_positions!(particles)
    L = boxsize(particles)
    for (particle, coordinates) in zip(particles, eachcol(L * rand(3, length(particles))))
        particle.r = coordinates
    end
    @assert unique(particles) == particles
    return particles
end

function reset_velocities!(particles)
    for particle in particles
        particle.v = zeros(MVector{3,Float64})
    end
    return particles
end

function reset!(particles)
    @assert length(particles) > 0
    reset_positions!(particles)
    reset_velocities!(particles)
    return particles
end

boxsize(particles) = cbrt(length(particles) / ρ)
